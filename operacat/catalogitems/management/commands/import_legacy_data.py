import csv
from collections import OrderedDict
import json
import re
from xml.etree import ElementTree as ET
from django.core.management.base import BaseCommand

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
        a_dict = OrderedDict()
        idnum = item.find("{http://operacat.uchicago.edu}IdNumber")
        composer = item.find("{http://operacat.uchicago.edu}composer")
        item_type = item.find("{http://operacat.uchicago.edu}itemType")
        place = item.find("{http://operacat.uchicago.edu}place")
        title = item.find("{http://operacat.uchicago.edu}title")
        start_date = item.find("{http://operacat.uchicago.edu}startDate")
        end_date = item.find("{http://operacat.uchicago.edu}endDate")
        date = item.find("{http://operacat.uchicago.edu}date")
        author_or_responsible = item.find("{http://operacat.uchicago.edu}authorOrResponsible")
        recipient_or_dedicatee = item.find("{http://operacat.uchicago.edu}recipientOrDedicatee")
        item_description = item.find("{http://operacat.uchicago.edu}itemDescription")
        item_notes = item.find("{http://operacat.uchicago.edu}itemNotes")
        id_links = item.find("{http://operacat.uchicago.edu}IdLinks")
        images = item.find("{http://operacat.uchicago.edu}images")
        for a_element in [idnum, composer, item_type, place, start_date, end_date, date,
                          author_or_responsible, recipient_or_dedicatee, title,
                          item_description, item_notes]:
            try:
                tag_name = a_element.tag.split("{http://operacat.uchicago.edu}")[1].strip()

                if tag_name == 'itemDescription':
                    #tag_value = [x.split('\n')[0].strip().lstrip() for x in stuff]
                    #tag_value = [x for x in tag_value if x != '']
                    string = ET.tostring(a_element)
                    string = re.sub(r"<ns0:itemDescription xmlns:ns0=\"http://operacat.uchicago.edu\">","", string.decode("utf-8"))
                    string = re.sub(r"</ns0:itemDescription>", "",string)
                    string = re.sub(r"<ns0:highlight>", "<b>", string)
                    string = re.sub(r"</ns0:highlight>", "</b>", string)
                    string_lists = string.split('\n')
                    string_lists = [x.strip().lstrip() for x in string_lists]
                    tag_value = ' '.join(string_lists)
                    highlights = a_element.findall("{http://operacat.uchicago.edu}highlight")
                    if len(highlights) > 0:
                        high_val = [x.text for x in highlights]
                        high_list_p = []
                        for n in high_val:
                            for p in n.split('\n'):
                                high_list_p.append(p.strip().lstrip())

                        a_dict["itemDescription_highlights"] = high_list_p
                    else:
                        a_dict["itemDescription_highlights"] = "None"
                elif  tag_name == 'itemNotes':
                    tag_value = [x.strip() for x in a_element.text.split('\n')]
                    tag_value = ' '.join([x for x in tag_value if x != ""])
                else:
                    if a_element.text != None:
                        tag_value = re.sub(r'\{|\}|\[|\]', '', a_element.text)
                        tag_value = re.split(';', tag_value)
                        tag_value = [x.strip().lstrip() for x in tag_value]
                        tag_value = [x for x in tag_value if 'etc' not in x]
                        tag_value = [x for x in tag_value if x != 'None']
                        tag_value = '; '.join(tag_value)
                    else:
                        tag_value = None
                a_dict[tag_name] = tag_value
            except AttributeError:
                pass
            a_dict_keys = list(a_dict.keys())

            for n_required in ['IdNumber', 'composer', 'itemType', 'place',
                               'startDate', 'endDate', 'date', "title",
                               'authorOrResponsible', 'recipientOrDedicatee',
                               'itemDescription', 'itemNotes', 'IdLinks', 'images']:
                if n_required not in a_dict_keys:
                    a_dict[n_required] = 'None'

        a_dict["dealer"] = ' '.join(dealer)
        a_dict["catalog"] = catalog
        a_dict["lot"] = lot
        try:
            idnum = int(a_dict["IdNumber"])
        except:
            idnum = 0
        if isinstance(idnum, str):
            idnum = 0
        a_dict["IdNumber"] = idnum
        for massageable in ["date", "endDate", "startDate", "place", "title",
                            "recipientOrDedicatee", "authorOrResponsible", "itemType"]:
            if a_dict.get(massageable, None):
                old_string = re.sub(r'\s{2,}', '',
                                    re.sub(r'\n', '',
                                           a_dict[massageable]))
                a_dict[massageable] = old_string
        if images:
            images = [x.text for x in images.findall("{http://operacat.uchicago.edu}image")]
            a_dict["images"] = '; '.join(images)
        if id_links:
            id_links = [x.text for x in id_links.findall("{http://operacat.uchicago.edu}IdLink")]
            a_dict["IdLinks"] = '; '.join(id_links)
        return a_dict

    def _extract_catalog_data(self, an_iterable, dealer_name):
        whole_list = []
        item_description_list = []
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
        item_description_list = []
        for n_source in all_sources:
            dealer_element = n_source.find("{http://operacat.uchicago.edu}dealer")
            dealer_info = self._find_dealer(dealer_element)
            catalog_root_element = dealer_element.find("{http://operacat.uchicago.edu}catalogues")
            iterable_catalogs = catalog_root_element.\
                findall("{http://operacat.uchicago.edu}catalogue")
            data += self._extract_catalog_data(iterable_catalogs, dealer_info)
        csv_record = []
        count = 0
        data = sorted(data, key=lambda x: x["IdNumber"])
        for n_item in data:
            if ',' in n_item["place"]:
                n_item["place"] = re.sub(',', ';', n_item["place"])
            if n_item["composer"] != "None":
                lookup = {'Rossini': 'Gioachino',
                          'Donizetti':'Gaetano',
                          'Bellini':'Vincenzo',
                          'Verdi':'Giuseppe',
                          'Puccini':'Giacomo'}
                n_item["composer"] =  n_item["composer"] + ", " + lookup[n_item["composer"]]
            count += 1
            dict_values = [value for key, value in n_item.items()]
            a_row = []
            for n_value in dict_values:
                if isinstance(n_value, list):
                    final = '\"' + '",\"'.join(n_value) + '\"'
                elif n_value:
                    final = n_value
                elif isinstance(n_value, int):
                    final = n_value
                else:
                    final = str(n_value)
                a_row.append(final)
            csv_record.append(a_row)
        csv_record = sorted(csv_record, key=lambda x: x[0])
        with open("../testdata/migration.csv", "w", encoding="utf-8") as write_file:
            csv_writer = csv.writer(write_file, delimiter=",",
                                    quotechar="\"",
                                    quoting=csv.QUOTE_ALL, lineterminator='\n')
            headers = ['IdNumber', 'composer', 'itemType', 'place', 'startDate',
                       'endDate', 'date', 'title', 'authorOrResponsible', 'recipientOrDedicatee',
                       'itemDescription', 'itemNotes', 'IdLinks', 'images', 'highlights',
                       'dealer', 'catalog', 'lot']
            csv_writer.writerow(headers)
            for record in csv_record:
                csv_writer.writerow(record)
        json.dump(data, open("../testdata/migration.json", "w", encoding="utf-8"),
                  indent=4)

