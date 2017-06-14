
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

    def handle(self, *args, **options):
    data = json.load(open(options["legacy_data_filepath"], "r",
                     encoding="utf-8"))
 
 
