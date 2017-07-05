import json
from django.core.management.base import BaseCommand

from catalogitems.models import CatalogItemPage, Dealer, Place


class Command(BaseCommand):
    """a management command to set lot information from legacy data

    This class will retrieve lot information for each item in legacy data and add
    it to the lot attribute of the corresponding item page
    """
    help = "Add lot information from legacy data to item pages"

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
        out the lot key:value.

        It then checks if there is a CatalogItemPage already present with that item
        in the title, and if there is it defines the lot attribute of that CatalogItemPage
        to be the value of the lot key:value pair from legacy data and saves the item page.
        """

        data = json.load(open(options["legacy_data_filepath"], "r",
                              encoding="utf-8"))
        for n in data:
            print(n["IdNumber"])
            cur = CatalogItemPage.objects.filter(title=n["IdNumber"])
            if cur.count() == 1:
                cur = cur[0]
                if n.get("lot", None):
                    if n["lot"] != "":
                        cur.lot = n["lot"]
                        cur.save()
