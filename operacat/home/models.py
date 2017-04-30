from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel

class TranslatedField(object):
    def __init__(self, en_field, it_field):
        self.en_field = en_field
        self.it_field = it_field

    def __get__(self, instance, owner):
        if translation.get_language() == 'it':
            return getattr(instance, self.it_field)
        else:
            return getattr(instance, self.en_field)

class HomePage(Page):

    content_panels = Page.content_panels 

class GenericPage(Page):
    body = RichTextField(blank=True, null=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
    ]

