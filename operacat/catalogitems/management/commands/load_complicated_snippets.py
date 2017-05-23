
from django.core.management.base import BaseCommand, CommandError
from catalogitems.models import CatalogItemPage, Place, Dealer, Composer
import json
from os.path import dirname, join

class Command(BaseCommand):
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
                 if n.get("place", None):

                if n.get("author or responsible", None):

                if n.get("recipient or dedicatee", None):


 