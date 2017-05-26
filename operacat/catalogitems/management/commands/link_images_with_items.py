
import json
from django.core.management.base import BaseCommand
from catalogimage.models import CatalogImage
from catalogitems.models import CatalogItemPage

class Command(BaseCommand):
    """a management command to interpret legacy data and link images to items

    This class is necessary for migrating part of legacy data into the operacat
    site.
    """
    help = "Link images stored in site with the right catalog item page"

    def add_arguments(self, parser):
        """the method that gets called to add parameter to the management command

        It takes a parser object and adds a string type argument called
        legacy_data_filepath
        """
        parser.add_argument("legacy_data_filepath",
                            help="Path to legacy data JSON", type=str)

    def handle(self, *args, **options):
        """the method that gets called to actually run the management command

        It opens the legacy_data_filepath parameter and loads it into a JSON
        object

        Then it iterates through the list of dicts in the data and selects
        out the image keys and item identifier key.

        It finds the CatalogItemPage that matches the item identifier and
        and if a matching CatalogItemPage can be found it continues. If not, it
        sends an error message to stderr

        It processes each item in the image to find the  matching CatalogImage
        object in the system to retrieve the primary key/id attribute to
        create stream_data dict item to append to stream_data list

        At end, it sets the stream_data to the matching CatalogItemPage
        images.stream_data attribute and saves the CatalogItemPage.
        """
        data = json.load(open(options["legacy_data_filepath"], "r",
                              encoding="utf-8"))
        for n_item in data:
            if n_item.get("images", None):
                cur = CatalogItemPage.objects.filter(title=n_item["item"])
                stream_val = []
                if cur.count() == 1:
                    cur = cur[0]
                    for n_image in n_image["images"]:
                        img_name = n_image["name"]
                        match = CatalogImage.objects.filter(title__contains=img_name)
                        if match.count() == 1:
                            img_id = match[0].id
                            val = {'type': 'images', 'value': img_id}
                            stream_val.append(val)
                    cur.images.stream_data = stream_val
                    cur.save()
                else:
                    self.stderr.write("{} is not present in system".format(n_item["item"]))
