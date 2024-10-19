from django.core.exceptions import ValidationError
from .snippets import ClaseColor
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from .blocks import NavegacionPrincipalBlock, ButtonBlock, TextBlock


class HomePage(Page):
    titulo = StreamField([
        ('texto', TextBlock()),
    ])
    descripcion = StreamField([
        ('texto', TextBlock()),
    ])
    boton = StreamField([
        ('boton', ButtonBlock()),  # Definirlo como un bloque dentro de StreamField
    ], blank=True)

    opciones_navegacion = StreamField([
        ('opcion_navegacion', NavegacionPrincipalBlock()),
    ], blank=True)


    content_panels = Page.content_panels + [
        FieldPanel('titulo'),
        FieldPanel('descripcion'),
        FieldPanel('boton'),
        FieldPanel('opciones_navegacion'),
    ]

    api_fields = [
        APIField('titulo'),
        APIField('descripcion'),
        APIField('boton'),
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

