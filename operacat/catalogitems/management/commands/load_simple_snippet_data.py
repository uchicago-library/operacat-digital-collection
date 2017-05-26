
import json
from django.core.management.base import BaseCommand

from catalogitems.models import CatalogItemPage, Catalog, Dealer, Composer, PieceTitle


class Command(BaseCommand):
    """a management command to set relationship information between items from legacy data

    This class will retrieve composer, catalog, dealer and optional piece title info
    for each item in legacy data and add each piece of info to the appropriate attribute
    on the corresponding item page
    """
    help = "Add simple snippet info from legacy data to item pages"

    def add_arguments(self, parser):
        """the method that gets called to add parameter to the management command

        It takes a parser object and adds a string type argument called
        legacy_data_filepath
        """
        parser.add_argument("legacy_data_filepath",
                            help="Path to legacy data JSON", type=str)

    def _switch_case(self, condition, query_string, current_object):
        def _build_title_query(query_param):
            return PieceTitle.objects.filter(name=query_param)

        def _build_composer_query(query_param):
            return Composer.objects.filter(last_name=query_param)

        def _build_catalog_query(query_param):
            return Catalog.objects.filter(catalog_name=query_param)

        def _build_dealer_query(query_param):
            return Dealer.objects.filter(dealer_name=query_param)

        if condition == 'composer':
            query = _build_composer_query(query_string)
        elif condition == 'title':
            query = _build_title_query(query_string)
        elif condition == 'dealer':
            query = _build_dealer_query(query_string)
        elif condition == 'catalog':
            query = _build_catalog_query(query_string)
        else:
            raise ValueError("invalid condition in _switch_case method")
        if query.count() == 1:
            if condition != 'title':
                setattr(current_object, condition, query[0])
                current_object.save()
            else:
                current_object.item_titles.create(a_title=query[0])

    def handle(self, *args, **options):
        """the method that gets called to actually run the management command

        It opens the legacy_data_filepath parameter and loads it into a JSON
        object

        Then it iterates through the list of dicts in the data and selects
        out the composer, dealer, catalog, and title key:value pairs.

        It then checks if there is a CatalogItemPage already present with that item
        in the title, and if there is it defines the relevant attributes for
        that CatalogItemPage with the appropriate key:value pair values.
        """

        data = json.load(open(options["legacy_data_filepath"], "r",
                              encoding="utf-8"))
        for n_item in data:
            cur = CatalogItemPage.objects.filter(title=n_item["item"])
            if cur.count() == 1:
                for n_condition in ['title', 'composer', 'catalog', 'dealer']:
                    self._switch_case(n_condition, n_item.get(n_condition, 'None'), cur[0])
            else:
                self.stderr.write("{} has no catalog item page".format(n_item["item"]))
