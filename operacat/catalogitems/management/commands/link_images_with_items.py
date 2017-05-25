
import json
from django.core.management.base import BaseCommand
from catalogimage.models import CatalogImage
from catalogitems.models import CatalogItemPage

class Command(BaseCommand):
    help = "Link images stored in site with the right catalog item page"

    def add_arguments(self, parser):
        parser.add_argument("legacy_data_filepath",
                            help="Path to legacy data JSON", type=str)

    def handle(self, *args, **options):
        data = json.load(open(options["legacy_data_filepath"], "r",
                              encoding="utf-8"))
        for n in data:
            if n.get("images", None):
                cur = CatalogItemPage.objects.filter(title=n["item"])
                stream_val = []
                if cur.count() == 1:
                    cur = cur[0]
                    for g in n["images"]:
                        img_name = g["name"]
                        match = CatalogImage.objects.filter(title__contains=img_name)
                        if match.count() == 1:
                            img_id = match[0].id
                            val = {'type': 'images', 'value': img_id}
                            stream_val.append(val)
                    cur.images.stream_data = stream_val
                    cur.save()
                else:
                    self.stderr.write("{} is not present in system".format(n["item"]))
