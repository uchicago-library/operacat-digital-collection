
import json
from django.core.management.base import BaseCommand

from catalogitems.models import CatalogItemPage, Place, Dealer,\
 Composer, AuthorOrResponsible, RecipientOrDedicatee


class Command(BaseCommand):
    """a management command to set relationship information between items from legacy data

    This class will retrieve item descriptoiun, and optional field note info
    for each item in legacy data and add each piece of info to the appropriate attribute
    on the corresponding item page
    """

    help = "Add item description and field notes from legacy data to item pages"

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
        out the field note, and item description key:value pairs.

        It then checks if there is a CatalogItemPage already present with that item
        in the title, and if there is it defines the relevant attributes for
        that CatalogItemPage with the appropriate key:value pair values.
        """
        data = json.load(open(options["legacy_data_filepath"], "r",
                              encoding="utf-8"))
        for n_item in data:
            cur = CatalogItemPage.objects.filter(title=n_item["item"])
            if cur.count() == 1:
                cur = cur[0]
                if n_item.get("item description", None):
                    val = n_item["item description"]
                    cur.item_description = "<p>" + val.strip() + "</p>"
                else:
                    self.stderr.write("{} has no item description".format(n_item["item"]))
                if n_item.get("item notes", None):
                    val = n_item["item notes"]
                    cur.field_notes = "<p>" + val.strip() + "</p>"
                cur.save()
