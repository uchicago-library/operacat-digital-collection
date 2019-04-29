"""the model definitions for item data
"""

from __future__ import absolute_import, unicode_literals

from django.db import models
from django.utils import translation
from django.utils.encoding import force_text
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet
from wagtail.core.models import Page, Orderable
from wagtail.core.blocks import CharBlock, PageChooserBlock,\
    StructBlock, RegexBlock, StreamBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel,\
    StreamFieldPanel, MultiFieldPanel
from wagtail.search import index


class TranslatedField(object):
    """class definition to translate page field values between English and
    Italian
    """
    def __init__(self, en_field, it_field):
        self.en_field = en_field
        self.it_field = it_field

    def __get__(self, instance, owner):
        if translation.get_language() == 'it':
            return getattr(instance, self.it_field)
        else:
            print(self.en_field)
            print(instance)
            return getattr(instance, self.en_field)


@register_snippet
class DealerCommonName(models.Model):
    common_name_text = models.CharField(max_length=255)

    search_fields = [index.FilterField("common_name_text")]

    def __str__(self):
        return "{}".format(self.common_name_text)


@register_snippet
class Dealer(models.Model):
    """the dealer snippet definition
    """
    the_name = models.CharField(max_length=255)
    common_name = models.ForeignKey('catalogitems.DealerCommonName',
                                    null=True,
                                    blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='+')
    panels = [
        FieldPanel("common_name"),
        FieldPanel("the_name"),
    ]
    search_fields = [index.FilterField("the_name")]

    def __str__(self):
        return "{}".format(self.the_name)


@register_snippet
class Catalog(models.Model):
    """the catalog snippet definition
    """
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
    """a composer snippet definition
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    panels = [
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
    """the place snippet definition
    """
    place_name = models.CharField(max_length=255)
    panels = [
        FieldPanel('place_name'),
    ]
    search_fields = [
        index.FilterField('place_name', partial_match=True),
    ]

    def __str__(self):
        return self.place_name


@register_snippet
class ItemType(models.Model):
    """the item type snippet defintion
    """
    # type_name_en = models.CharField(max_length=255)
    # type_name_it = models.CharField(max_length=255)

    type_name = models.CharField(max_length=255)
    panels = [
        FieldPanel('type_name'),
    ]
    search_fields = [
        index.FilterField('type_name', partial_match=True),
    ]

    def __str__(self):
        return self.type_name


@register_snippet
class AuthorOrResponsible(models.Model):
    """the author or responsible snippet definition
    """
    author_name = models.CharField(max_length=255)
    optional_title = models.CharField(max_length=1000, blank=True, null=True)
    panels = [
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
    """the recipient or dedicatee snippet defintion
    """
    recipient_name = models.CharField(max_length=255)
    panels = [
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
    """the musical piece title snippet definition
    """
    name = models.CharField(max_length=1000)
    panels = [
        FieldPanel("name"),
    ]
    search_fields = [
        index.FilterField('name', partial_match=True),
    ]

    def __str__(self):
        return self.name


class ItemTypeOrderable(Orderable):
    """a class defintion to allow item types to be added in a m2m fashion to a
    particular page
    """
    a_type = models.ForeignKey(
        ItemType,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=("Item Type")
    )
    a_record = ParentalKey(
        'catalogitems.CatalogItemPage',
        on_delete=models.CASCADE,
        related_name='item_types'
    )
    panels = [
        FieldPanel("a_type"),
    ]


class PlaceOrderable(Orderable):
    """a class defintion to allow places to be added m2m to a particular page
    """
    a_place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=("A Place")
    )
    place_record = ParentalKey(
        'catalogitems.CatalogItemPage',
        on_delete=models.CASCADE,
        related_name='item_places'
    )
    panels = [
        FieldPanel("a_place"),
    ]


class PieceTitleOrderable(Orderable):
    """a class defintion to allow piece titles to be added m2m to a particular
    page
    """
    a_title = models.ForeignKey(
        PieceTitle,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=("A Title")
    )
    piece_record = ParentalKey(
        'catalogitems.CatalogItemPage',
        on_delete=models.CASCADE,
        related_name='item_titles'
    )
    panels = [
        FieldPanel("a_title"),
    ]


class AuthorOrResponsibleOrderable(Orderable):
    """a class defintion to allow author/responsible entities to be added m2m
    to a page
    """
    an_author = models.ForeignKey(
        AuthorOrResponsible,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=("An Item Author Or Responsible")
    )
    author_record = ParentalKey(
        'catalogitems.CatalogItemPage',
        on_delete=models.CASCADE,
        related_name='item_authororesposibles'
    )
    panels = [
        FieldPanel("an_author"),
    ]


class RecipientOrDedicateeOrderable(Orderable):
    """a class defintion to allow recipient/dedicatee entities to be added m2m
    to a page
    """
    a_recipient = models.ForeignKey(
        RecipientOrDedicatee,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=("An Item Recipient Or Dedicatee")
    )
    recipient_record = ParentalKey(
        'catalogitems.CatalogItemPage',
        on_delete=models.CASCADE,
        related_name='item_recipientordedicatees'
    )
    panels = [
        FieldPanel("a_recipient"),
    ]


class CatalogItemPage(Page):
    """the definition for an item record page which is the centerpiece of the
    site
    """
    item_catalog = models.ForeignKey(
        'catalogitems.Catalog',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    item_dealer = models.ForeignKey(
        'catalogitems.Dealer',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    item_composer = models.ForeignKey(
        'catalogitems.Composer',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    lot = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    date_label = models.CharField(
        "Date",
        blank=True,
        max_length=200,
        null=True
    )
    start_date_day = models.IntegerField(
        blank=True,
        null=True
    )
    start_date_month = models.IntegerField(
        blank=True,
        null=True
    )
    start_date_year = models.IntegerField(
        blank=True,
        null=True
    )
    end_date_day = models.IntegerField(
        blank=True,
        null=True
    )
    end_date_month = models.IntegerField(
        blank=True,
        null=True
    )
    end_date_year = models.IntegerField(
        blank=True,
        null=True
    )
    images = StreamField(
        [('images', ImageChooserBlock())],
        blank=True,
        null=True
    )
    item_description = RichTextField(
        blank=True,
        null=True
    )
    field_notes = RichTextField(
        blank=True,
        null=True
    )
    related_items = StreamField(
        [(
            'related_item',
            PageChooserBlock(target_model='catalogitems.CatalogItemPage')
        )],
        blank=True,
        null=True
    )
    content_panels = Page.content_panels + [
        SnippetChooserPanel("item_dealer"),
        SnippetChooserPanel("item_catalog"),
        SnippetChooserPanel("item_composer"),
        FieldPanel('lot'),
        FieldPanel("date_label"),
        MultiFieldPanel([
            FieldPanel("start_date_day"),
            FieldPanel("start_date_month"),
            FieldPanel("start_date_year"),
        ], heading="Start Date"),
        MultiFieldPanel([
            FieldPanel("end_date_day"),
            FieldPanel("end_date_month"),
            FieldPanel("end_date_year"),
        ], heading="End Date"),
        InlinePanel(
            'item_types',
            label="Item Types"
        ),
        InlinePanel(
            "item_places",
            label="Item Places"
        ),
        InlinePanel(
            "item_titles",
            label="Item Titles"
        ),
        InlinePanel(
            "item_authororesposibles",
            label="Author or Responsible"
        ),
        InlinePanel(
            "item_recipientordedicatees",
            label="Recipient Or Dedicatee"
        ),
        StreamFieldPanel("images"),
        StreamFieldPanel("related_items"),
        FieldPanel('item_description'),
        FieldPanel('field_notes')
    ]
    search_fields = Page.search_fields + [
        index.SearchField("date_label"),
        index.SearchField("lot"),
        index.SearchField(
            'title',
            partial_match=True
        ),
        index.SearchField(
            'item_description',
            partial_match=True
        ),
        index.SearchField(
            'field_notes',
            partial_match=True
        ),
    ]
