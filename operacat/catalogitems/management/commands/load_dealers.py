
import json
from django.core.management.base import BaseCommand
from wagtail.wagtailcore.models import Page

from catalogitems.models import Dealer, CatalogItemPage, DealerCommonName
from home.models import GenericPage

class Command(BaseCommand):
    """a management command to create initial migration of items from legacy data

    This class is necessary for a starting the migration of legacy data into the system.
    """
    help = "Add item pages for every item in legacy data to system"

    def add_arguments(self, parser):
        """the method that gets called to add parameter to the management command

        It takes a parser object and adds a string type argument called
        legacy_data_filepath
        """
        parser.add_argument("legacy_data_filepath",
                            help="Path to legacy data JSON", type=str)

    def handle(self, *args, **options):
        """the method that gets called to actually run the management command

        It opens the legacy_data_filepath parameter and loads it into a JSON
        object

        Then it iterates through the list of dicts in the data and selects
        out the item key:value.

        It then checks if there is a CatalogItemPage already present with that item
        in the title, and if ther is not it creates one and adds it to the system
        as a child of the home page.
        """
        data = json.load(open(options["legacy_data_filepath"], "r",
                              encoding="utf-8"))
        count = 0
        for n_item in data:
            count += 1
            new_dealer = n_item["dealer"]
            if 'Douot' in new_dealer:
                common_name = DealerCommonName.objects.filter(common_name_text='Douot')[0]
            elif 'Drouot' in new_dealer:
                common_name = DealerCommonName.objects.filter(common_name_text='Douot')[0]
            elif 'Christie' in new_dealer:
                common_name = DealerCommonName.objects.filter(common_name_text='Christie')[0]
            elif 'Sotheby' in new_dealer:
                common_name = DealerCommonName.objects.filter(common_name_text='Sotheby')[0]
            else:
                common_name = DealerCommonName()
                common_name.common_name_text = new_dealer
                common_name.save()
                common_name = common_name

            check_for_existing_record = Dealer.objects.filter(the_name=new_dealer)
            if check_for_existing_record.count() == 0:
                new = Dealer()
                new.common_name = common_name
                new.the_name = new_dealer
                new.save()
            else:
                new = check_for_existing_record[0]
                new.common_name = common_name
                new.save()
            cur = CatalogItemPage.objects.filter(title=n_item["IdNumber"])
            if cur.count() == 1:
                cur = cur[0]
                cur.item_dealer = new
                cur.save()
