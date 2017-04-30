
import json

from catalogitems.models import ItemTypeOrderable, PlaceOrderable, PieceTitleOrderable, ItemType, CatalogItemPage, Dealer, PieceTitle, Composer, Catalog, Place, RecipientOrDedicatee, AuthorOrResponsible, AuthorOrResponsibleOrderable, RecipientOrDedicateeOrderable

from wagtail.wagtailcore.models import Page

class LoadData(object):
    def __init__(self):
        self.data = json.load(open("/home/tdanstrom/src/apps/operacat_migrations/all_items_for_operacat.json", "r"))
        self.home = Page.objects.all()[2]

    def  load_data(self):
        home = Page.objects.all()[2]
        count = 6
        for n_thing in self.data:
            new_item = CatalogItemPage()
            new_item.title = n_thing["item"]
            new_item.slug = "item-" + str(count)
            if n_thing.get("item description", None):
                new_item.item_description = n_thing["item description"]
            if n_thing.get("item notes", None):
                new_item.field_notes = n_thing["item notes"]
            if n_thing.get("composer", None):
                composer = n_thing["composer"]
                the_composer = Composer.objects.filter(last_name=composer)[0]
                new_item.item_composer = the_composer
            if n_thing.get("dealer", None):
                dealer = n_thing["dealer"]
                the_dealer = Dealer.objects.filter(dealer_name=n_thing["dealer"])[0]
                new_item.item_dealer = the_dealer
            if n_thing.get("catalog", None):
                catalog = n_thing["catalog"]
                the_catalog = Catalog.objects.filter(catalog_name=n_thing["catalog"])[0]
                new_item.item_catalog = the_catalog
            type_list = []
            if n_thing.get("item type", None):
                types = n_thing["item type"]
                for n_type in types:
                    a_type = ItemType.objects.filter(type_name=n_type)[0]
                    type_list.append(a_type)
            place_list = []
            if n_thing.get("place", None):
                for n_place in n_thing["place"]:
                    a_place = Place.objects.filter(place_name=n_place)[0]
                    place_list.append(a_place)
            titles_list = []
            if n_thing.get("title", None):
                a_title = PieceTitle.objects.filter(name=n_thing["title"])[0]
                titles_list.append(a_title)
            author_list = []
            if n_thing.get("author or responsible", None):
                for n_author in n_thing["author or responsible"]:
                    a_author = AuthorOrResponsible.objects.filter(author_name=n_author["name"])[0]
                    author_list.append(a_author)
            recipient_list = []
            if n_thing.get("recipient or dedicatee", None):
                for n_recipient in n_thing["recipient or dedicatee"]:
                    a_recipient = RecipientOrDedicatee.objects.filter(recipient_name=n_recipient["name"])[0]
                    recipient_list.append(a_recipient)
            new_item.lot = n_thing["lot"]
            new_saved = self.home.add_child(instance=new_item)
            for n_place in place_list:
                new = PlaceOrderable()
                new.a_place = n_place
                new.place_record = new_saved
                new.save()
            for n_type in type_list:
                new = ItemTypeOrderable()
                new.a_type = n_type
                new.a_record = new_saved
                new.save()
            for n_title in titles_list:
                new = PieceTitleOrderable()
                new.a_title = n_title
                new.piece_record = new_saved
                new.save()
            for n_recipient in recipient_list:
                new = RecipientOrDedicateeOrderable()
                new.a_recipient = n_recipient
                new.recipient_record = new_saved
                new.save()
            for n_author in author_list:
                new = AuthorOrResponsibleOrderable()
                new.an_author = n_author
                new.author_record = new_saved
                new.save()
            count += 1

