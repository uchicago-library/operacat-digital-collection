
import json
from django.core.management.base import BaseCommand
from wagtail.core.models import Page
import re

from catalogitems.models import Place, CatalogItemPage

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
            new_places = n_item["place"]
            new_places = re.sub(r'\{|\}|\[|\]|\?','',new_places)
            new_places = re.split(',|;', new_places)
            new_places = [x.strip().lstrip() for x in new_places]
            new_places = [x for x in new_places if 'etc' not in x]
            new_places = [x for x in new_places if x != 'None']
            a_list = []
            for a_place in new_places:
                check_for_existing_record = Place.objects.filter(place_name=a_place)
                if check_for_existing_record.count() == 0:
                     new = Place()
                     new.place_name = a_place
                     new.save()
                     a_list.append(new.place_name)
                else:
                     a_list.append(check_for_existing_record[0].place_name)
                     self.stderr.write("{} already exists in database.\n".format(a_place))
            print(a_list)
            cur = CatalogItemPage.objects.filter(title=n_item["IdNumber"])
            if cur.count() == 1:
                cur = cur[0]
                for n_place in a_list:
                    a = Place.objects.filter(place_name=n_place)[0]
                    cur.item_places.create(a_place=a)
                cur.save()
