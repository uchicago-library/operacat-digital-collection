
from django.core.management.base import BaseCommand, CommandError
from catalogitems.models import CatalogItemPage, Catalog, Dealer, Composer
import json
from os.path import dirname, join

class Command(BaseCommand):k
    help = "Add related item info from legacy data to new OperaCat website"

    def add_arguments(self, parser):
        parser.add_argument("legacy_data_filepath",
                            help="Path to legacy data JSON", type=str)

    def handle(self, *args, **options):
        data = json.load(open(options["legacy_data_filepath"], "r",
                              encoding="utf-8"))
        successful = open(join(dirname(options["legacy_data_filepath"]),
                               'successful.txt'), "w")
        counter = 0
        total = 0
        all_available = 0
        for n in data:
            cur = CatalogItemPage.objects.filter(title=n["item"])
            if cur.count() == 1:
               cur = cur[0]
               if n.get("title"):
                    try:
                        matching_title = PieceTitle.objects.filter(name=n["title"])
                        if matching_title.count() == 1:
                            cur.item_titles.create(a_title=matching_title[0])
                        else:
                            self.stderr("{} could not be found in system.".format(n.get('title')))
                    except KeyError:
                        self.stderr.write("{} piece title is not in system.".format(n["title"]))
               matching_catalog = Catalog.objects.filter(catalog_name=n["catalog"])
               matching_dealer = Dealer.objects.filter(dealer_name=n["dealer"])
               try:
                   matching_composer = Composer.objects.filter(last_name=n["composer"])
               except KeyError:
                   self.stderr.write("{} has no composer".format(n["item"]))
               if matching_catalog.count() == 1:
                   cur.item_catalog = matching_catalog[0]
               if matching_dealer.count() == 1:
                   cur.item_dealer = matching_dealer[0]
               if matching_composer.count() == 1:
                   cur.item_composer = matching_composer[0]
               cur.save()
            else:
                self.stderr.write("{} has no catalog item page".format(n["item"]))
 