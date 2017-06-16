
import json
from django.core.management.base import BaseCommand
from wagtail.wagtailcore.models import Page

from catalogitems.models import Dealer

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
        for n_item in data:
            new_dealer = n_item["dealer"]
            if new_dealer != 'None':
                check_for_existing_record = Dealer.objects.filter(the_name=' '.join(new_dealer))
                if check_for_existing_record.count() == 0:
                    new = Dealer()
                    new.the_name = ' '.join(new_dealer)
                    new.save()
                else:
                    self.stderr.write("{} already exists in database.\n".format(' '.join(new_dealer)))
