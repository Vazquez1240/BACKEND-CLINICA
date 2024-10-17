from django.core.exceptions import ValidationError
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api import APIField
from wagtail.blocks import ChoiceBlock, StructBlock, BooleanBlock


class PredefinedNavigationOptionBlock(StructBlock):
    opcion = ChoiceBlock(choices=[
        ('nosotros', 'Nosotros'),
        ('servicios', 'Servicios'),
        ('galeria', 'Galeria'),
        ('contacto', 'Contacto'),
        # Añade más opciones si lo deseas
    ], required=True, help_text="Selecciona una opción de navegación",)

    activo = BooleanBlock(required=True, default=True, help_text="¿Está activo?")

class HomePage(Page):
    titulo = RichTextField(blank=True)
    descripcion = RichTextField(blank=True)
    opciones_navegacion = StreamField([
        ('opcion_navegacion', PredefinedNavigationOptionBlock()),
    ], blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('titulo'),
        FieldPanel('descripcion'),
        FieldPanel('opciones_navegacion'),
    ]

    api_fields = [
        APIField('titulo'),
        APIField('descripcion'),
        APIField('opciones_navegacion'),
    ]

    def clean(self):
        super().clean()
        opciones = [block.value['opcion'] for block in self.opciones_navegacion if block.value['activo']]

        # Verifica que el número de opciones esté entre 1 y 4
        if len(opciones) < 1:
            raise ValidationError("Debes seleccionar al menos 1 opción.")
        if len(opciones) > 4:
            raise ValidationError("Solo puedes seleccionar hasta 4 opciones.")

        # Verifica que las opciones no se repitan
        if len(opciones) != len(set(opciones)):
            raise ValidationError("Las opciones no pueden repetirse.")