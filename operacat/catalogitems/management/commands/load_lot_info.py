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
            cur = CatalogItemPage.objects.filter(title=n["item"])[0]
            if n.get("lot", None):
                if n["lot"] != "":
                    cur.lot = n["lot"]
                    cur.save()
                    print(cur.lot)
