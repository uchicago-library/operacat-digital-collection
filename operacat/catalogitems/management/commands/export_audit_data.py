
import csv
from django.core.management.base import BaseCommand
from wagtail.wagtailimages.models import Image

from catalogimage.models import CatalogImage
from catalogitems.models import CatalogItemPage

class Command(BaseCommand):
    """a management command to retrieve catalog item data and write it to a CSV file

    This class is necessary for generating a CSV file that can be audited.
    """

    help = "A management command to export data from catalogitems into a CSV file"

    def add_arguments(self, parser):
        """the method that gets called to add parameter to the management command

        It takes a parser object and adds a string type argument called
        legacy_data_filepath
        """
        parser.add_argument("output_filepath",
                            help="Path to save the CSV file", type=str)


    def handle(self, *args, **options):
        """the method that gets called to actually run the management command
        """
        all_items = CatalogItemPage.objects.all()
        lines = []
        for n_item in all_items:
            composer = n_item.item_composer.last_name if n_item.item_composer else "not defined"
            catalog = n_item.item_catalog.catalog_name if n_item.item_catalog else "not defined"
            dealer = n_item.item_dealer.the_name if n_item.item_dealer else "not defined"
            lot = n_item.lot
            item_related_items = [x['value'] for x in n_item.related_items.stream_data]
            item_images = [x['value'] for x in n_item.images.stream_data]
            images = []
            if item_images:
                for n in item_images:
                    a_img = Image.objects.filter(id=n)
                    if a_img.count() == 1:
                        images.append(a_img[0].title)
            images = ','.join(images) if images else "not defined"
            rel_items = []
            if item_related_items:
                for n in item_related_items:
                    match = CatalogItemPage.objects.filter(id=n)
                    if match.count() == 1:
                        rel_items.append(match[0].title)
            rel_items = ','.join(rel_items) if rel_items else "not defined"
            item_id = n_item.title
            item_desc = n_item.item_description.strip() if n_item.item_description \
                                                        else "not defined"
            item_note = n_item.field_notes.strip() if n_item.field_notes else "not defined"
            item_date_info = n_item.date_information
            item_places = ','.join([x.a_place.place_name \
                                for x in n_item.item_places.all()])
            item_types = ','.join([x.a_type.type_name \
                                for x in n_item.item_types.all()])
            item_authors = ','.join([x.an_author.author_name \
                                    for x in n_item.item_authororesposibles.all()])
            item_recipients = ','.join([x.a_recipient.recipient_name \
                                 for x in n_item.item_recipientordedicatees.all()])
            item_titles = ','.join([x.a_title.name \
                                for x in n_item.item_titles.all()])
            end_dates = []
            start_dates = []
            dates = []
            date_labels = []
            for date_bit in item_date_info.stream_data:
                bit_type = date_bit["type"]
                bit_value = date_bit["value"]
                if bit_type == 'end_date':
                    end_dates.append(bit_value["month"] + '/' +\
                                     bit_value["day"] + '/' + bit_value["year"])
                if bit_type == 'start_date':
                    start_dates.append(bit_value["month"] + '/' +\
                                       bit_value["day"] + '/' + bit_value["year"])
                if bit_type == 'date':
                    dates.append(bit_value["month"] + '/' +\
                                 bit_value["day"] + '/' + bit_value["year"])
                if bit_type == 'date_label':
                    date_labels.append(bit_value["date_label"])
            end_dates = ','.join(end_dates)
            start_dates = ','.join(start_dates)
            dates = ','.join(dates)
            date_labels = ','.join(date_labels)
            line = [item_id,
                    composer,
                    catalog,
                    dealer,
                    lot,
                    item_places,
                    item_types,
                    item_authors,
                    item_recipients,
                    item_titles,
                    item_desc,
                    item_note,
                    rel_items,
                    images
                   ]
            lines.append(line)
        with open(options["output_filepath"], "w", encoding="utf-8", newline="") as write_file:
            csv_writer = csv.writer(write_file, delimiter=",",
                                    quotechar="\"", quoting=csv.QUOTE_ALL)
            csv_writer.writerow(["item", "composer", "catalog", "dealer", "lot",
                                 "places", "types", "authors", "recipients",
                                 "titles", "description", "field note", "related items", "images"])
            for a_line in lines:
                csv_writer.writerow(a_line)
