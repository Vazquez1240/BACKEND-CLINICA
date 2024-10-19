from wagtail.blocks import ChoiceBlock, StructBlock, BooleanBlock, URLBlock, CharBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets import blocks
from .snippets import ClaseColor


class NavegacionPrincipalBlock(StructBlock):
    opcion = ChoiceBlock(choices=[
        ('Nosotros', 'Nosotros'),
        ('Servicios', 'Servicios'),
        ('Galeria', 'Galeria'),
        ('Contacto', 'Contacto'),
        # Añade más opciones si lo deseas
    ], required=True, help_text="Selecciona una opción de navegación",)

    activo = BooleanBlock(required=False,  default=False, help_text="¿Está activo?")

    url = URLBlock(help_text='ingrese la pagina a la que va (Ejemplo si es el de servicio seria /servicios)', required=True)



class ImageBlock(StructBlock):
    imagen = ImageChooserBlock(required=True)

    class Meta:
        icon = 'image'
        label = 'Imagen'

class ButtonBlock(StructBlock):
    accion_tipo = ChoiceBlock(required=True, choices=[
        ('', 'Tipo de acción'),
        ('sin_accion', 'Sin acción'),
        ('pagina', 'Página'),
        ('url', 'URL'),
    ])
    texto = CharBlock(required=True)
    color_texto = blocks.SnippetChooserBlock(ClaseColor, required=False, default='primary')
    ruta = CharBlock(required=True)

    color = blocks.SnippetChooserBlock(ClaseColor, required=False, default='primary')

    class Meta:
        icon = 'button'
        label = 'Botón'


class TextBlock(StructBlock):
    texto = CharBlock(required=True)
    color_texto = blocks.SnippetChooserBlock(ClaseColor, required=False, default='primary')

    class Meta:
        icon = 'text'
        label = 'Texto'