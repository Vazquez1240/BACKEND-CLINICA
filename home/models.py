from django.core.exceptions import ValidationError
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from .blocks import NavegacionPrincipal



class HomePage(Page):
    titulo = RichTextField(blank=True)
    descripcion = RichTextField(blank=True)

    opciones_navegacion = StreamField([
        ('opcion_navegacion', NavegacionPrincipal()),
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

        if len(opciones) < 1:
            raise ValidationError("Debes seleccionar al menos 1 opción.")
        if len(opciones) > 4:
            raise ValidationError("Solo puedes seleccionar hasta 4 opciones.")


        if len(opciones) != len(set(opciones)):
            raise ValidationError("Las opciones no pueden repetirse.")