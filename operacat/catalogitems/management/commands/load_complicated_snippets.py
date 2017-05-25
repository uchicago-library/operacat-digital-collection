
import json
from django.core.management.base import BaseCommand
from catalogitems.models import CatalogItemPage, Place,\
    AuthorOrResponsible, RecipientOrDedicatee, ItemType


class Command(BaseCommand):
    """a management command to load migrate m2m field definition from legacy data
    """
    help = "Add m2m relation snippet information from legacy data to pages"

    def add_arguments(self, parser):
        parser.add_argument("legacy_data_filepath",
                            help="Path to legacy data JSON", type=str)

    def _add_place_info(self, place_list, cur):
        for place in set(place_list):
            pl_name = place
            pl_record = Place.objects.filter(place_name=pl_name)
            if pl_record.count() == 1:
                cur.item_places.create(a_place=pl_record[0])
        return cur

    def _add_recipients(self, rec_list, cur):
        for recipient in rec_list:
            re_name = recipient["name"]
            re_record = RecipientOrDedicatee.objects.\
                filter(recipient_name=re_name)
            if re_record.count() == 1:
                cur.item_recipientordedicatees.\
                    create(a_recipient=re_record[0])
        return cur

    def _add_authors(self, author_list, cur):
        for author in author_list:
            au_name = author["name"]
            au_record = AuthorOrResponsible.objects.\
                filter(author_name=au_name)
            if au_record.count() == 1:
                cur.item_authororesposibles.\
                    create(an_author=au_record[0])
        return cur

    def _add_item_types(self, type_list, cur):
        for a_type in type_list:
            ty_name = a_type
            ty_record = ItemType.objects.filter(type_name=ty_name)
            if ty_record.count() == 1:
                cur.item_types.create(a_type=ty_record[0])
        return cur

    def handle(self, *args, **options):
        data = json.load(open(options["legacy_data_filepath"], "r",
                              encoding="utf-8"))
        for n_thing in data:
            cur = CatalogItemPage.objects.filter(title=n_thing["item"])
            if cur.count() == 1:
                cur = cur[0]
                if n_thing.get("author or responsible", None):
                    self._add_authors(n_thing["author or responsible"], cur)
                if n_thing.get("recipient or dedicatee", None):
                    self._add_recipients(n_thing["recipient or dedicatee"],
                                         cur)
                if n_thing.get("place", None):
                    self._add_place_info(n_thing["place"], cur)
                if n_thing.get("item type", None):
                    self._add_item_types(n_thing["item type"], cur)
                cur.save()
