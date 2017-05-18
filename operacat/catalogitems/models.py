from __future__ import absolute_import, unicode_literals
from django.db import models
from django import forms
from django.utils import translation

import uuid
from modelcluster.fields import ParentalKey

from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.blocks import ChoiceBlock, CharBlock,\
 DateBlock, PageChooserBlock, RichTextBlock, StructBlock, RegexBlock, ChooserBlock
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.fields import ImageField
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailsearch import index

@register_snippet
class Dealer(models.Model):
    dealer_name = models.CharField(max_length=255)

    panels = [
        FieldPanel("dealer_name"),
    ]

    search_fields = [index.FilterField("dealer_name", partial_match=True)]

    def __str__(self):
        return "{}".format(self.dealer_name)


@register_snippet
class Catalog(models.Model):
    catalog_name = models.CharField(max_length=255)
    panels = [
        FieldPanel("catalog_name")
    ]
    search_fields = [
        index.FilterField("catalog_name", partial_match=True)
    ]

    def __str__(self):
        return "{}".format(self.catalog_name)

@register_snippet
class Composer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel('first_name'),
        FieldPanel('last_name'),
    ]

    search_fields = [
        index.FilterField('first_name', partial_match=True),
        index.FilterField('last_name', partial_match=True),
    ]

    def __str__(self):
        return "{}, {}".format(self.last_name, self.first_name)

@register_snippet
class Place(models.Model):
    place_name = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel('place_name'),
    ]

    search_fields = [
        index.FilterField('place_name', partial_match=True),
    ]

    def __str__(self):
        return self.place_name

@register_snippet
class ItemType(models.Model):
    type_name = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel('type_name')
    ]

    search_fields = [
        index.FilterField('name', partial_match=True),
    ]

    def __str__(self):
        return self.type_name

@register_snippet
class AuthorOrResponsible(models.Model):
    author_name = models.CharField(max_length=255)
    optional_title = models.CharField(max_length=1000, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('author_name'),
        FieldPanel('optional_title'),
    ]

    search_fields = [
        index.FilterField('author_name', partial_match=True),
    ]

    def __str__(self):
        return self.author_name

@register_snippet
class RecipientOrDedicatee(models.Model):
    recipient_name = models.CharField(max_length=255)

    panels = Page.content_panels + [
        FieldPanel('recipient_name'),
    ]

    search_fields = [
        index.FilterField('recipient_name', partial_match=True),
    ]

    search_fields = [
        index.FilterField('recipient_name', partial_match=True),
    ]

    def __str__(self):
        return self.recipient_name

@register_snippet
class PieceTitle(models.Model):
    name = models.CharField(max_length=1000)

    content_panels = Page.content_panels + [
        FieldPanel("name"),
    ]


    search_fields = [
        index.FilterField('name', partial_match=True),
    ]

    def __str__(self):
        return self.name

class TranslatedField(object):
    def __init__(self, en_field, it_field):
        self.en_field = en_field
        self.it_field = it_field

    def __get__(self, instance, owner):
        if translation.get_language() == 'it':
            return getattr(instance, self.it_field)
        else:
            return getattr(instance, self.en_field)

class ItemTypeOrderable(Orderable):
    a_type = models.ForeignKey(ItemType, related_name='+', verbose_name=("Item Type"))
    a_record = ParentalKey('catalogitems.CatalogItemPage', related_name='item_types')

    panels = [
        FieldPanel("a_type"),
    ]


class PlaceOrderable(Orderable):
    a_place = models.ForeignKey(Place, related_name='+', verbose_name=("A Place"))
    place_record = ParentalKey('catalogitems.CatalogItemPage', related_name='item_places')

    panels = [
        FieldPanel("a_place"),
    ]

class PieceTitleOrderable(Orderable):
    a_title = models.ForeignKey(PieceTitle, related_name='+', verbose_name=("A Title"))
    piece_record = ParentalKey('catalogitems.CatalogItemPage', related_name='item_titles')

    panels = [
        FieldPanel("a_title"),
    ]

class AuthorOrResponsibleOrderable(Orderable):
    an_author = models.ForeignKey(AuthorOrResponsible, related_name='+', verbose_name=("An Item Author Or Responsible "))
    author_record = ParentalKey('catalogitems.CatalogItemPage', related_name='item_authororesposibles')

    panels = [
        FieldPanel("an_author"),
    ]

class RecipientOrDedicateeOrderable(Orderable):
    a_recipient = models.ForeignKey(RecipientOrDedicatee, related_name='+', verbose_name=("An Item Author Or Responsible "))
    recipient_record = ParentalKey('catalogitems.CatalogItemPage', related_name='item_recipientordedicatees')

    panels = [
        FieldPanel("a_recipient"),
    ]



class DateEntryBlock(StructBlock):
    month = RegexBlock(regex='^\d{2}$', error_message="Not a valid month input. It must be two digits. If month numeral is only a single place a zero at the front of the number as in '01'")
    day = RegexBlock(regex='^\d{2}$', error_message="Not a valid month input. It must be two digits. If month numeral is only a single place a zero at the front of the number as in '01'")
    year = RegexBlock(regex='^\d{4}$', error_message="Not a valid year. It must be a four numeral digit as in 1967")

    class Meta:
        icon = 'date'
        template = 'blocks/date_entry_block.html'

class DateLabelEntryBlock(StructBlock):
    date_label = CharBlock(max_length=100)

    class Meta:
        icon = 'date'
        template = 'blocks/datelabel_entry_block.html'

class CatalogItemPage(Page):
    item_catalog = models.ForeignKey('catalogitems.Catalog',
                                     null=True,
                                     blank=True,
                                     on_delete=models.SET_NULL,
                                     related_name='+')
    item_dealer = models.ForeignKey('catalogitems.Dealer',
                                     null=True,
                                     blank=True,
                                     on_delete=models.SET_NULL,
                                     related_name='+')
    item_composer = models.ForeignKey('catalogitems.Composer',
                                      null=True,
                                      blank=True,
                                      on_delete=models.SET_NULL,
                                      related_name='+')
    lot = models.CharField(max_length=100, blank=True, null=True)
    date_information = StreamField([
        ('date_label', DateLabelEntryBlock()),
        ('date', DateEntryBlock(label="Date for Item")),
        ('start_date', DateEntryBlock(label="Start Date")),
        ('end_date', DateEntryBlock(label="End Date"))], blank=True, null=True)
    images = StreamField([('images', ImageChooserBlock())], blank=True, null=True)
    item_description = RichTextField(blank=True, null=True)
    field_notes = RichTextField(blank=True, null=True)
    related_items = StreamField([('related_item', PageChooserBlock(target_model='catalogitems.CatalogItemPage'))], blank=True, null=True)

    content_panels = Page.content_panels + [
        SnippetChooserPanel("item_dealer"),
        SnippetChooserPanel("item_catalog"),
        SnippetChooserPanel("item_composer"),
        FieldPanel('lot'),
        StreamFieldPanel('date_information'),
        InlinePanel('item_types', label="Item Types"),
        InlinePanel("item_places", label="Item Places"),
        InlinePanel("item_titles", label="Item Titles"),
        InlinePanel("item_authororesposibles", label="Author or Responsible"),
        InlinePanel("item_recipientordedicatees", label="Recipient Or Dedicatee"),
        StreamFieldPanel("images"),
        StreamFieldPanel("related_items"),
        FieldPanel('item_description'),
        FieldPanel('field_notes')
    ]
    search_fields = Page.search_fields + [
        index.SearchField("item_composer"),
        index.SearchField("item_catalog"),
        index.SearchField("item_dealer"),
        index.FilterField("lot"),
	index.FilterField('title', partial_match=True),
        index.SearchField('item_description', partial_match=True),
        index.SearchField('field_notes', partial_match=True),
    ]

