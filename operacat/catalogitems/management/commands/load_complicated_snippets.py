
from django.core.management.base import BaseCommand, CommandError
from catalogitems.models import CatalogItemPage, Place, Dealer,\
 Composer, AuthorOrResponsible, RecipientOrDedicatee, ItemType
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
            if cur.count() == 1:
                cur = cur[0]
                if n.get("place", None):
                    for p in n["place"]:
                        place_rec = Place.objects.filter(place_name=p)
                        if place_rec.count() == 1:
                            cur.item_places.create(a_place=place_rec[0])
                if n.get("author or responsible", None):
                    for au in n["author or responsible"]:
                        au_name = au["name"]
                        au_record = AuthorOrResponsible.objects.filter(author_name=au_name)
                        if au_record.count() == 1:
                            cur.item_authororesposibles.create(an_author=au_record[0])
                            print(cur.item_authororesposibles.all())
                if n.get("recipient or dedicatee", None):

                    for re in n["recipient or dedicatee"]:
                        re_name = re["name"]
                        re_record = RecipientOrDedicatee.objects.filter(recipient_name=re_name)
                        if re_record.count() == 1:
                            cur.item_recipientordedicatees.create(a_recipient=re_record[0])
                if n.get("place", None):
                    for pl in n["place"]:
                        pl_name = pl
                        print(pl_name)
                        pl_record = Place.objects.filter(place_name=pl_name)
                        if pl_record.count() == 1:
                            cur.item_places.create(a_place=pl_record[0])
                if n.get("item type", None):
                    for ty in n["item type"]:
                        ty_name = ty
                        ty_record = ItemType.objects.filter(type_name=ty_name)
                        if ty_record.count() == 1:
                            cur.item_types.create(a_type=ty_record[0])
                cur.save()