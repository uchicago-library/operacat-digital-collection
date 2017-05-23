
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.blocks import ChoiceBlock, CharBlock,\
 DateBlock, PageChooserBlock, RichTextBlock, StructBlock, RegexBlock, ChooserBlock
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.fields import ImageField
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailsearch import index

from catalogitems.models import PieceTitle

# Create your models here.

class DateLabelEntryBlock(StructBlock):
    date_label = CharBlock(max_length=100)

    class Meta:
        icon = 'date'

class DateEntryBlock(StructBlock):
    month = RegexBlock(regex='^\d{2}$', error_message="Not a valid month input. It must be two digits. If month numeral is only a single place a zero at the front of the number as in '01'")
    day = RegexBlock(regex='^\d{2}$', error_message="Not a valid month input. It must be two digits. If month numeral is only a single place a zero at the front of the number as in '01'")
    year = RegexBlock(regex='^\d{4}$', error_message="Not a valid year. It must be a four numeral digit as in 1967")

    class Meta:
        icon = 'date'

class CustomOrderable(Orderable):
    custom_title = models.ForeignKey(PieceTitle, related_name='+', verbose_name=("A Title"))
    custom_record = ParentalKey('customtype.CustomType', related_name='custom_titles')
    panels = [
        FieldPanel("custom_title"),
    ]

class CustomType(Page):
    item_catalog = models.ForeignKey('catalogitems.Catalog',
                                     null=True,
                                     blank=True,
                                     on_delete=models.SET_NULL,
                                     related_name='+')
    date_information = StreamField([
        ('date_label', DateLabelEntryBlock()),
        ('date', DateEntryBlock(label="Date for Item")),
        ('start_date', DateEntryBlock(label="Start Date")),
        ('end_date', DateEntryBlock(label="End Date"))], blank=True, null=True)

    related_items = StreamField([('related_item',
                                  PageChooserBlock(target_model=\
                                    'customtype.CustomType'))],
                                                   blank=True, null=True)

    content_panels = Page.content_panels + [
        SnippetChooserPanel("item_catalog"),
        StreamFieldPanel("related_items"),
        StreamFieldPanel("date_information"),
        InlinePanel("custom_titles", label="Custom Titles"),
    ]
