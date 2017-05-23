from django.db import models
from wagtail.wagtailimages import Image

# Create your models here.

class CatalogImage(Image):
    embargoed = models.BooleanField(default=True)
    alternative_text = models.CharField(max_length=100)

    content_panels = Image.content_panels + [
        FieldPanel("alternative_text"),
        FieldPanel("embargoed")
    ]