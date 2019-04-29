
import json
from django.core.management.base import BaseCommand
from wagtail.core.models import Page
import re

from catalogitems.models import PieceTitle, CatalogItemPage

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
            new_piece_titles = n_item["title"]
            if new_piece_titles != None:
                new_piece_titles = re.sub(r'\{|\}|\[|\]|\?', '', new_piece_titles)
                new_piece_titles = re.split(r'\;', new_piece_titles)
                new_piece_titles = [x.strip().lstrip() for x in new_piece_titles]
                new_piece_titles = [x for x in new_piece_titles if 'etc' not in x]
                new_piece_titles = [x for x in new_piece_titles if x != 'None']
                a_list = []
                for a_title in new_piece_titles:
                    check_for_existing_record = PieceTitle.objects.filter(name=a_title)
                    if check_for_existing_record.count() == 0:
                        new = PieceTitle()
                        new.name = a_title
                        new.save()
                        a_list.append(new.name)
                    else:
                        a_list.append(check_for_existing_record[0].name)
                        self.stderr.write("{} already exists in database.\n".format(a_title))
            cur = CatalogItemPage.objects.filter(title=n_item["IdNumber"])
            if cur.count() == 1:
                cur = cur[0]
                for n_title in a_list:
                    a = PieceTitle.objects.filter(name=n_title)[0]
                    cur.item_titles.create(a_title=a)
                cur.save()


