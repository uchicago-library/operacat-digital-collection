
import json
from django.core.management.base import BaseCommand

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
            the_id = n_item["item"]
            cur = CatalogItemPage.objects.filter(title=the_id)
            if cur.count() == 1:
                cur = cur[0]
                if n_item.get("date info", None):
                    final_output = self._extract_date_parts(n_item["date info"])
                    cur.date_information.stream_data = final_output
                    cur.save()
                else:
                    self.stderr.write("{} has no date information to add".\
                        format(the_id))
            else:
                self.stderr.write("{} has no catalog item page".\
                    format(the_id))
