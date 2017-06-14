import csv
import json
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
        dealer_text = dealer.text
        dealer_text_parts = dealer_text.split('\n')
        dealer = [x.strip().lstrip() for x in dealer_text_parts]
        return [x for x in dealer if x != b'']

    def _find_catalog_name(self, catalog_element):
        text_data = catalog_element.text.strip()
        if text_data == "":
            return None
        else:
            return text_data

    def  _convert_an_item(self, dealer, catalog, lot, item):
        a_dict = {}
        idnum = item.find("{http://operacat.uchicago.edu}IdNumber")
        composer = item.find("{http://operacat.uchicago.edu}composer")
        item_type = item.find("{http://operacat.uchicago.edu}itemType")
        place = item.find("{http://operacat.uchicago.edu}place")
        start_date = item.find("{http://operacat.uchicago.edu}startDate")
        end_date = item.find("{http://operacat.uchicago.edu}endDate")
        date = item.find("{http://operacat.uchicago.edu}date")
        author_or_responsible = item.find("{http://operacat.uchicago.edu}authorOrResponsible")
        recipient_or_dedicatee = item.find("{http://operacat.uchicago.edu}recipientOrDedicatee")
        item_description = item.find("{http://operacat.uchicago.edu}itemDescription")
        item_notes = item.find("{http://operacat.uchicago.edu}itemNotes")
        id_links = item.find("{http://operacat.uchicago.edu}IdLinks")
        images = item.find("{http://operacat.uchicago.edu}images")
        if images:
            images = [x.text for x in images.findall("{http://operacat.uchicago.edu}image")]
            a_dict["images"] = images

        if id_links:
            id_links = [x.text for x in id_links.findall("{http://operacat.uchicago.edu}IdLink")]
            a_dict["idLinks"] = id_links
        a_dict["dealer"] = dealer
        a_dict["catalog"] = catalog
        a_dict["lot"] = lot
        for a_element in [idnum, composer, item_type, place, start_date, end_date, date,
                          author_or_responsible, recipient_or_dedicatee,
                          item_description, item_notes]:
            try:
                tag_name = a_element.tag.split("{http://operacat.uchicago.edu}")[1].strip()
                tag_value = a_element.text
                if tag_name == 'itemDescription' or tag_name == 'itemNotes':
                    tag_value = [x.strip() for x in tag_value.split('\n')]
                    tag_value = [x for x in tag_value if x != ""]
                a_dict[tag_name] = tag_value
            except AttributeError:
                pass
            a_dict_keys = list(a_dict.keys())
            for n_required in ['IdNumber', 'composer', 'itemType', 'place',
                               'startDate', 'endDate', 'date',
                               'authorOrResponsible', 'recipientOrDedicatee',
                               'itemDescription', 'itemNotes', 'IdLinks', 'images']:
                if n_required not in a_dict_keys:
                    a_dict[n_required] = 'None'
        return a_dict

    def _extract_catalog_data(self, an_iterable, dealer_name):
        whole_list = []
        count = 0
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
                for n_item in items:
                    i = self._convert_an_item(dealer_name,
                                              catalog_name,
                                              lot_name,
                                              n_item)
                    whole_list.append(i)
        return whole_list

    def handle(self, *args, **options):
        data = ET.parse(options["legacy_data_filepath"])
        data_root = data.getroot()
        all_sources = data_root.findall("{http://operacat.uchicago.edu}source")
        data = []
        for n_source in all_sources:
            dealer_element = n_source.find("{http://operacat.uchicago.edu}dealer")
            dealer_info = self._find_dealer(dealer_element)
            catalog_root_element = dealer_element.find("{http://operacat.uchicago.edu}catalogues")
            iterable_catalogs = catalog_root_element.\
                findall("{http://operacat.uchicago.edu}catalogue")
            data += self._extract_catalog_data(iterable_catalogs, dealer_info)

        csv_record = []
        for n_item in data:
            row = []
            for key in n_item:
                value = n_item[key]
                if isinstance(value, list):
                    value = ','.join(value)
                else:
                    value = value
                row.append(value)
                csv_record.append(row)
        with open("csv_data", "w", encoding="utf-8") as write_file:
            csv_writer = csv.writer(write_file, delimiter=",",
                                    quotechar="\"",
                                    quoting=csv.QUOTE_ALL)
            for record in csv_record:
                csv_writer.writerow(record)
        json.dump(data, open("./foo.json", "w", encoding="utf-8"),
                  indent=4)
