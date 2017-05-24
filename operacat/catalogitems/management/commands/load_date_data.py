
from django.core.management.base import BaseCommand, CommandError
from catalogitems.models import CatalogItemPage
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
                if n.get("date info", None):
                    date_labels = n["date info"].get("date_label", None)
                    end_dates = n["date info"].get("end date", None)
                    start_dates = n["date info"].get("start date", None)
                    dates = n["date info"].get("date", None)
                    date_values = []
                    if date_labels:
                        for dl in date_labels:
                            a_val = {'type': 'date_label', 'value': dl}
                            date_values.append(a_val)
                    else:
                        a_val = {'type': 'date_label', 'value': 's.d.'}
                        print(a_val)
                        date_values.append(a_val)
                    if dates:
                        for d in dates:
                            if type(d) != type([]):
                                pulled_val_parts = d.split('/')
                                if len(pulled_val_parts) == 3:
                                    d_val = {'type': 'end_date',
                                             'value':{'year': pulled_val_parts[2],
                                                      'day': pulled_val_parts[1],
                                                      'month': pulled_val_parts[0]}}
                                    date_values.append(d_val)
                    if end_dates:
                        for ed in end_dates:
                            pulled_val_parts = ed.split('/')
                            if len(pulled_val_parts) == 3:
                                ed_val = {'type': 'end_date',
                                          'value':{'year': pulled_val_parts[2],
                                                   'day': pulled_val_parts[1],
                                                   'month': pulled_val_parts[0]}}
                                date_values.append(ed_val)
                    if start_dates:
                        for sd in start_dates:
                            pull_val_parts = sd.split('/')
                            if len(pulled_val_parts) == 3:
                                sd_val = {'type': 'start_date',
                                          'value':{'year': pulled_val_parts[2],
                                                   'day': pulled_val_parts[1],
                                                   'month': pulled_val_parts[0]}}
                                date_values.append(sd_val)
                    cur.date_information.stream_data = date_values
                    print(cur.date_information.stream_data)
                    cur.save()
                else:
                    self.stderr.write("{} has no date information to add".\
                        format(n["item"]))
            else:
                self.stderr.write("{} has no catalog item page".\
                    format(n["item"]))
