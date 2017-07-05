
import json
import csv
from django.core.management.base import BaseCommand
import re

from catalogitems.models import CatalogItemPage

class Command(BaseCommand):
    """a management command to migrate date field definition from legacy data

    This class is necessary for adding all dates -- date_labels, date,
    start_date, and end_date -- to item pages in the system
    """

    help = "Add date information from legacy data to relevant pages"

    def add_arguments(self, parser):
        """the method that gets called to add parameter to the management command

        It takes a parser object and adds a string type argument called
        legacy_data_filepath
        """
        parser.add_argument("legacy_data_filepath",
                            help="Path to legacy data JSON", type=str)

    def _extract_date_string_parts(self, some_string):
        val_parts = some_string.split('/')
        if len(val_parts) == 3:
            return val_parts
        else:
            return None

    def _extract_date_parts(self, date_blob):
        def _iterate_a_list_of_values(a_list, type_string):
            def _build_stream_value(type_string, value):
                def _make_date_entry(value):
                    return {'year': value[2], 'month': value[1],
                            'day': value[0] if len(str(value[0])) == 2 else str(value[0]).zfill(1)}
                output = {'type': type_string}
                if type_string in ['date', 'end_date', 'starrt_date']:
                    output['value'] = _make_date_entry(value)
                else:
                    output['value'] = value
                return output

            output = []
            for an_item in a_list:
                output.append(_build_stream_value(type_string, an_item))
            return output

        date_labels = date_blob["date info"].get("date_label", None)
        end_dates = date_blob["date info"].get("end date", None)
        start_dates = date_blob["date info"].get("start date", None)
        dates = date_blob["date info"].get("date", None)
        final_output = []
        if date_labels:
            final_output += _iterate_a_list_of_values(date_labels, 'date_label')
        else:
            a_val = {'type': 'date_label',
                     'value': {'date_label': 's.d.'}}
            final_output.append(a_val)
        if dates:
            final_output += _iterate_a_list_of_values(dates, 'date')
        if end_dates:
            final_output += _iterate_a_list_of_values(end_dates,
                                                      'end_date')
        if start_dates:
            final_output += _iterate_a_list_of_values(start_dates,
                                                      'start_date')
        return final_output

    def _sanitize(self, some_string):
        if isinstance(some_string, str):
            new_output = re.sub(r'\{|\}|\[|\]', '', some_string)
            new_output = re.split(',|;', new_output)
            new_output = [x for x in new_output if 'etc' not in x]
            new_output = [x for x in new_output if x != 'None']
            return ','.join(new_output)
        else:
            return None

    def handle(self, *args, **options):
        """the method that gets called to actually run the management command

        It opens the legacy_data_filepath parameter and loads it into a JSON
        object

        Then it iterates through the list of dicts in the data and selects
        out the date-info key:value.

        It finds the CatalogItemPage that matches the item identifier and
        and if a matching CatalogItemPage can be found it continues. If not, it
        sends an error message to stderr

        It sends value of author responsible to private method _add_authors,
        recipient dedicatee value to _add_recipients, place value
        to _add_places, and item types to _add_item_types

        At end, it sets the stream_data to the matching CatalogItemPage
        date_information.stream_data attribute and saves the CatalogItemPage.
        """
        data = json.load(open(options["legacy_data_filepath"], "r",
                              encoding="utf-8"))
        for n_item in data:
            the_id = n_item["IdNumber"]
            matched_item = CatalogItemPage.objects.filter(title=the_id)
            if matched_item.count() == 1:
                date = n_item["date"]
                date = self._sanitize(date)
                end_date = n_item["endDate"]
                end_date = self._sanitize(end_date)
                start_date = n_item["startDate"]
                start_date = self._sanitize(start_date)
                matched_item = matched_item[0]
                if date:
                    date_value = date
                    matched_item.date_label = date_value
                    matched_item.save()
                else:
                    matched_item.date = 's.d.'
                    matched_item.save()
                if end_date:
                    parts = re.split(r'\/|-', end_date)
                    if re.compile(r'\d{4}').match(parts[0]):
                        day = parts[2]
                        month = parts[1]
                        year = parts[0]
                    else:
                        day = parts[0]
                        month = parts[1]
                        year = parts[2]
                    if re.compile(r'\d{4}').match(year):
                        matched_item.end_date_day = day
                        matched_item.end_date_month = month
                        matched_item.save()
                if start_date:
                    parts = re.split(r'\/|-', start_date)
                    if re.compile(r'\d{4}').match(parts[0]):
                        day = parts[2]
                        month = parts[1]
                        year = parts[0]
                    else:
                        day = parts[0]
                        month = parts[1]
                        year = parts[2]
                    if re.compile(r'\d{4}').match(year):
                        matched_item.start_date_day = day
                        matched_item.start_date_month = month
                        matched_item.save()

