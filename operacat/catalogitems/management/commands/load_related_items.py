
import json
from django.core.management.base import BaseCommand

from catalogitems.models import CatalogItemPage


class Command(BaseCommand):
    """a management command to set relationship information between items from legacy data

    This class will retrieve relationship information for each item in legacy data and add
    it to the related_items attribute of the corresponding item page
    """

    help = "Add related item info from legacy data to new OperaCat website"

    def add_arguments(self, parser):
        """the method that gets called to add parameter to the management command

        It takes a parser object and adds a string type argument called
        legacy_data_filepath
        """
        parser.add_argument("legacy_data_filepath", help="Path to legacy data JSON", type=str)

    def _bundle_relation_statements(self, list_of_relations):
        output = []
        for a_relation in list_of_relations:
            related_item = CatalogItemPage.objects.filter(title=a_relation)
            if related_item.count() == 1:
                stream_value = {'type': 'related_item', 'value': related_item[0].id}
                output.append(stream_value)
        return output

    def handle(self, *args, **options):
        """the method that gets called to actually run the management command

        It opens the legacy_data_filepath parameter and loads it into a JSON
        object

        Then it iterates through the list of dicts in the data and selects
        out the 'related item' key:value.

        It then checks if there is a CatalogItemPage already present with that item
        in the title, and if there is it defines the related_items.stream_data attribute of
        that CatalogItemPage to be the value of the related_item key:value pair from
        legacy data and saves the item page.
        """

        data = json.load(open(options["legacy_data_filepath"], "r", encoding="utf-8"))
        counter = 0
        total = 0
        all_available = 0
        for n_item in data:
            all_available += 1
            current = CatalogItemPage.objects.filter(title=n_item["item"])
            if current.count() == 1:
                total += 1
                current = current[0]
                if n_item.get("related items", None):
                    stream_data = self._bundle_relation_statements(n_item["related items"])
                    current.related_items.stream_data = stream_data
                    current.save()
                    counter += 1
                else:
                    self.stderr.write("{} has no related items".format(current.title))
            else:
                self.stderr.write("{} has no corresponding catalog item page.".\
                   format(n_item["item"]))
        conclusion = "{} records modified out of {} total potentially".format(counter, total) +\
                     "modifiable records from {}".format(all_available) +\
                     "total records in legacy data\n"
        self.stdout.write(conclusion)
