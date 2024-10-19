from wagtail.snippets.models import register_snippet
from django.db import models
from wagtail.api import APIField

@register_snippet
class ClaseColor(models.Model):
    nombre = models.CharField(max_length=120, primary_key=True)

    api_fields = [
        APIField("nombre"),
    ]

    def __str__(self):
        return self.nombre