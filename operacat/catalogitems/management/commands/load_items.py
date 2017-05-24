
import json
from django.core.management.base import BaseCommand, CommandError 
from os.path import dirname, join
from wagtail.wagtailcore.models import Page

from catalogitems.models import CatalogItemPage, Dealer, Place


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
        home = Page.objects.filter(title="Home")[0]
        for n in data:
             if n["item"]:
                cur = CatalogItemPage.objects.filter(title=n["item"])
                if cur.count() == 1:
                    cur = cur[0]
                else:
                    cur = CatalogItemPage()
                    cur.title = n["item"]
                    home.add_child(instance=cur)
             else:
                 self.stderr.write(str(n))