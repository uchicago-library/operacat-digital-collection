
from django.core.management.base import BaseCommand, CommandError
from catalogitems.models import CatalogItemPage
import json
from os.path import dirname, join

class Command(BaseCommand):
    help = "Add related item info from legacy data to new OperaCat website"

    def add_arguments(self, parser):
        parser.add_argument("legacy_data_filepath", help="Path to legacy data JSON", type=str)

    def handle(self, *args, **options):
        data = json.load(open(options["legacy_data_filepath"], "r", encoding="utf-8"))
        successful = open(join(dirname(options["legacy_data_filepath"]), 'successful.txt'), "w")
        for n in data:
            current = CatalogItemPage.objects.filter(title=n["item"])
            if current.count() == 1:
                 current = current[0]
                 if n.get("related items", None):
                     rels = []
                     for g in n["related items"]:
                         match = CatalogItemPage.objects.filter(title=g)
                         if match.count() == 1:
                             match = match[0]
                             val = {'type': 'related_item', 'value': match.id}
                             rels.append(val)

                     successful.write("{}\n".format(current.title))
                     current.related_items.stream_data = rels
                     current.save()
                 else:
                    pass
                     #self.stderr.write("{} has no related items".format(current.title))
            else:
                pass
                 #self.stderr.write("{} has no corresponding catalog item page.".format(n["item"]))

