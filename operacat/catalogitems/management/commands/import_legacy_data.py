
from xml.etree import ElementTree as ET
from django.core.management.base import BaseCommand
from sys import stderr

class Command(BaseCommand):
    """a management command to set relationship information between items from legacy data

    This class will retrieve item descriptoiun, and optional field note info
    for each item in legacy data and add each piece of info to the appropriate attribute
    on the corresponding item page
    """

    help = "Add item description and field notes from legacy data to item pages"

    def add_arguments(self, parser):
        """the method that gets called to add parameter to the management command

        It takes a parser object and adds a string type argument called
        legacy_data_filepath
        """
        parser.add_argument("legacy_data_filepath",
                            help="Path to legacy data XML file", type=str)
        return parser

    def _find_dealer(self, dealer):
        dealer_text = dealer.text.encode('-utf-8')
        dealer_text_parts = dealer_text.split(b'\n')
        dealer = [x.strip().lstrip() for x in dealer_text_parts]
        return [x for x in dealer if x != b'']

    def _find_catalog_name(self, catalog_element):
        text_data = catalog_element.text.strip()
        if text_data == "":
            return None
        else:
            return text_data

    def _extract_catalog_data(self, an_iterable, dealer_name):
        for n_iterable in an_iterable:
            catalog_name = self._find_catalog_name(n_iterable)
            lots_element = n_iterable.find("{http://operacat.uchicago.edu}lots")
            lots = lots_element.findall("{http://operacat.uchicago.edu}lot")
            for n_lot in lots:
                lot_name = n_lot.text.strip()
                if lot_name == "":
                    lot_name = 's.n.'
                else:
                    lot_name = lot_name
                items = n_lot.findall("{http://operacat.uchicago.edu}item")
                print(dealer_name)
                print(catalog_name)
                print(lot_name)
                print(items)

    def handle(self, *args, **options):
        data = ET.parse(options["legacy_data_filepath"])
        data_root = data.getroot()
        all_sources = data_root.findall("{http://operacat.uchicago.edu}source")
        for n_source in all_sources:
            dealer_element = n_source.find("{http://operacat.uchicago.edu}dealer")
            dealer_info = self._find_dealer(dealer_element)
            catalog_root_element = dealer_element.find("{http://operacat.uchicago.edu}catalogues")
            iterable_catalogs = catalog_root_element.findall("{http://operacat.uchicago.edu}catalogue")
            self._extract_catalog_data(iterable_catalogs, dealer_info)
