from django.db.models.signals import post_delete
from django.db import models
from django.dispatch import receiver

from wagtail.images.models import AbstractImage, Image, AbstractRendition


class CatalogImage(AbstractImage):
    embargo = models.NullBooleanField(default=True)
    alt_text = models.CharField(max_length=100, blank=True, null=True)

    admin_form_fields = Image.admin_form_fields + (
        'embargo',
        'alt_text',
    )


class CatalogRendition(AbstractRendition):
    image = models.ForeignKey(
        CatalogImage,
        on_delete=models.CASCADE,
        related_name='renditions'
    )

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )


@receiver(post_delete, sender=CatalogImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)


@receiver(post_delete, sender=CatalogRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)
