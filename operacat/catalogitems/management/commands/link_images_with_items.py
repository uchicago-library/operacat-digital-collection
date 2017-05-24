
from django.core.management.base import BaseCommand, CommandError
from catalogitems.models import CatalogItemPage, Place, Dealer,\
 Composer, AuthorOrResponsible, RecipientOrDedicatee, ItemType
import json
from os.path import dirname, join

class Command(BaseCommand):
    help = "Link images stored in site with the right catalog item page"

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
            if n.get("images", None):
                for g in n["images"]:
                    img_name = g["name"]
                    match = Image.objects.filter(title__contains=img_name)
                    if match.count() == 1:
                        pass
                    else:
                        self.stderr.write("{} does not exist in the system.".format(img_name))