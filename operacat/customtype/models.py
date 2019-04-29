from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.blocks import ChoiceBlock, CharBlock,\
 DateBlock, PageChooserBlock, RichTextBlock, StructBlock, RegexBlock, ChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.fields import ImageField
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.search import index

from catalogitems.models import PieceTitle

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
    custom_title = models.ForeignKey(
        PieceTitle,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=("A Title")
    )
    custom_record = ParentalKey(
        'customtype.CustomType',
        on_delete=models.CASCADE,
        related_name='custom_titles'
    )
    panels = [
        FieldPanel("custom_title"),
    ]

class CustomType(Page):
    item_catalog = models.ForeignKey(
        'catalogitems.Catalog',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    date_information = StreamField([
        ('date_label', DateLabelEntryBlock()),
        ('date', DateEntryBlock(label="Date for Item")),
        ('start_date', DateEntryBlock(label="Start Date")),
        ('end_date', DateEntryBlock(label="End Date"))], blank=True, null=True)

    related_items = StreamField([('related_item',
                                  PageChooserBlock(target_model=\
                                    'customtype.CustomType'))],
                                                   blank=True, null=True)

    sample_text_field = RichTextField(default="this is an item description")
    content_panels = Page.content_panels + [
        SnippetChooserPanel("item_catalog"),
        StreamFieldPanel("related_items"),
        StreamFieldPanel("date_information"),
        InlinePanel("custom_titles", label="Custom Titles"),
        FieldPanel("sample_text_field"),
    ]
