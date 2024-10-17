from wagtail.blocks import ChoiceBlock, StructBlock, BooleanBlock, URLBlock


class NavegacionPrincipal(StructBlock):
    opcion = ChoiceBlock(choices=[
        ('Nosotros', 'Nosotros'),
        ('Servicios', 'Servicios'),
        ('Galeria', 'Galeria'),
        ('Contacto', 'Contacto'),
        # Añade más opciones si lo deseas
    ], required=True, help_text="Selecciona una opción de navegación",)

    activo = BooleanBlock(required=False,  default=False, help_text="¿Está activo?")

    url = URLBlock(help_text='ingrese la pagina a la que va (Ejemplo si es el de servicio seria /servicios)', required=True)