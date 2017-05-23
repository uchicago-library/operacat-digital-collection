
from django.core.management.base import BaseCommand, CommandError
from catalogitems.models import CatalogItemPage
import json

class AddRelatedItems(BaseComment):
    help = "Reads related item info from legacy data and migrates it to the operacat website"

    def add_arguments(self, parser):
        parser.add_arguments('legacy_data_file', type=str)

    def handle(self, *args, **options):
        print(options)
        return "hi"

# data = json.load(open("all_items_for_operacat.json", "r", encoding="utf-8"))

# successful = open("passed.txt", "a", encoding="utf-8")

# for n in data:
#     current = CatalogItemPage.objects.filter(title=n)
#     if current.count() == 1:
#         current = current[0]
#         if n.get("related items", None):
#             rels = []
#             for g in n["related items"]:
#                 match = CatalogItemPage.objects.filter(title=g)
#                 if match.count() == 1:
#                     match = match[0]
#                     val = {'type': 'related_item', 'value': match.id}
#                     rels.append(val)
#             successful.write("{}\n".format(current.title))
#             current.related_items.stream_data = rels
#             current.save()
#         else:
#             stderr.write("{} has no related items".format(current.title))
#     else:
#         stderr.write("{} has no corresponding catalog item page.".format(n["item"]))
