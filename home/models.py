from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api import APIField

class HomePage(Page):
    titulo = RichTextField(blank=True)
    descripcion = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('titulo'),
        FieldPanel('descripcion'),
    ]

    api_fields = [
        APIField('titulo'),
        APIField('descripcion'),
    ]
