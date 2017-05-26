
import json
from django.core.management.base import BaseCommand
from catalogitems.models import CatalogItemPage, Place,\
    AuthorOrResponsible, RecipientOrDedicatee, ItemType


class Command(BaseCommand):
    """a management command to load migrate m2m field definition from legacy data

    This class is necessary for adding places, authorOrResponsible,
    recipientOrDedicatee and itemType information from legacy data to item pages
    in the system
    """
    help = "Add m2m relation snippet information from legacy data to pages"

    def add_arguments(self, parser):
        """the method that gets called to add parameter to the management command

        It takes a parser object and adds a string type argument called
        legacy_data_filepath
        """
        parser.add_argument("legacy_data_filepath",
                            help="Path to legacy data JSON", type=str)

    def _add_place_info(self, place_list, cur):
        """a method to iterate a list of place names and add them to an item page

        place_list = list of strings
        cur = an instance of CatalogItemPage

        This method iterates over a list of place names, finds the matching Place
        snippet in the system and adds the the Place instance to the item_places
        attribute of the relevant CatalogItemPage object
        """
        for place in set(place_list):
            pl_name = place
            pl_record = Place.objects.filter(place_name=pl_name)
            if pl_record.count() == 1:
                cur.item_places.create(a_place=pl_record[0])
        return cur

    def _add_recipients(self, rec_list, cur):
        """a method to iterate a list of recipients and add them to an item page

        rec_list = list of dicts
        cur = an instance of CatalogItemPage

        This method iterates over a list of recipient dicts, finds the matching
        RecipientOrDedicatee snippet in the system and adds the
        RecipientOrDedicatee instance to the item_recipientordedicatee attribute of the
        relevant CatalogItemPage object
        """
        for recipient in rec_list:
            re_name = recipient["name"]
            re_record = RecipientOrDedicatee.objects.\
                filter(recipient_name=re_name)
            if re_record.count() == 1:
                cur.item_recipientordedicatees.\
                    create(a_recipient=re_record[0])
        return cur

    def _add_authors(self, author_list, cur):
        """a method to iterate a list of recipients and add them to an item page

        rec_list = list of dicts
        cur = an instance of CatalogItemPage

        This method iterates over a list of recipient dicts, finds the matching
        AuthorOrResponsible snippet in the system and adds the
        AuthorOrResponsible instance to the item_authororresposibles attribute of the
        relevant CatalogItemPage object
        """

        for author in author_list:
            au_name = author["name"]
            au_record = AuthorOrResponsible.objects.\
                filter(author_name=au_name)
            if au_record.count() == 1:
                cur.item_authororesposibles.\
                    create(an_author=au_record[0])
        return cur

    def _add_item_types(self, type_list, cur):
        """a method to iterate a list of recipients and add them to an item page

        type_list = list of strings
        cur = an instance of CatalogItemPage

        This method iterates over a list of type names, finds the matching
        Itemtyupe snippet in the system and adds the
        ItemType instance to the item_types attribute of the
        relevant CatalogItemPage object
        """


        for a_type in type_list:
            ty_name = a_type
            ty_record = ItemType.objects.filter(type_name=ty_name)
            if ty_record.count() == 1:
                cur.item_types.create(a_type=ty_record[0])
        return cur

    def handle(self, *args, **options):
        """the method that gets called to actually run the management command

        It opens the legacy_data_filepath parameter and loads it into a JSON
        object

        Then it iterates through the list of dicts in the data and selects
        out the author responsible, recipient dedicatee, place and item type
        keys.

        It finds the CatalogItemPage that matches the item identifier and
        and if a matching CatalogItemPage can be found it continues. If not, it
        sends an error message to stderr

        It sends value of author responsible to private method _add_authors,
        recipient dedicatee value to _add_recipients, place value
        to _add_places, and item types to _add_item_types

        At end, it sets the stream_data to the matching CatalogItemPage
        images.stream_data attribute and saves the CatalogItemPage.
        """
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
