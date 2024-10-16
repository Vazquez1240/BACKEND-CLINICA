from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index
from wagtail.fields import StreamField
from wagtail.api import APIField
from wagtail import blocks as core_blocks


class EnlaceBlock(core_blocks.StructBlock):
    titulo = core_blocks.CharBlock()
    tipo = core_blocks.ChoiceBlock(choices=[('pagina', 'Página'), ('url', 'URL'), ('sin_enlace', 'Sin Enlace')],
                                   default='pagina')
    pagina = core_blocks.PageChooserBlock(null=True, blank=True, required=False)
    url = core_blocks.URLBlock(null=True, blank=True, required=False)

    class Meta:
        icon = 'link'
        label = 'Enlace'
        classname = 'enlace'
        form_classname = 'enlace'
        api_fields = [
            APIField("titulo"),
            APIField("tipo"),
            APIField("pagina"),
            APIField("url"),
        ]



class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    footer = StreamField([
        ('ColumnaTexto', core_blocks.StructBlock([
            ('titulo', core_blocks.CharBlock()),
            ('texto', core_blocks.RichTextBlock()),
        ])),
        ('ColumnaLinks', core_blocks.StructBlock([
            ('enlace', core_blocks.ListBlock(EnlaceBlock(), min_num=1, max_num=6)),
        ])),
        ('Licencia', core_blocks.StructBlock([
            ('texto', core_blocks.RichTextBlock()),
        ], null=True)),
    ], block_counts={
        'ColumnaTexto': {'min_num': 0, 'max_num': 3},
        'ColumnaLinks': {'min_num': 0, 'max_num': 1},
        'Licencia': {'min_num': 1, 'max_num': 1},
    }, use_json_field=True, default=None)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
        FieldPanel('footer'),
    ]

class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

