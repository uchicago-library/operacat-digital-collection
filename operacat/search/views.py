from __future__ import absolute_import, unicode_literals

from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from sys import stderr

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query
from wagtail.wagtailsearch.backends import get_search_backend

from catalogitems.models import  *

def search(request):
    search_query = request.GET.get('query', None)
    page_num = int(request.GET.get("page", 1))
    if search_query:
        search_results = CatalogItemPage.objects.order_by('title').live().search(search_query)
        #query = Query.get(search_query)
        #query.add_hit()
    else:
        search_results = CatalogItemPage.objects.none()
    total_results = search_results.count()
    paginator = Paginator(search_results, 100)
    if page_num == 1:
        start_pointer = 1
        if total_results - ((page_num * 100) - 100) < 100:
            end_pointer = total_results
        else:
             end_pointer = 100
    elif total_results - ((page_num * 100) - 100) < 100:
        start_pointer = (page_num * 100) - 100
        end_pointer = total_results
    else:
        start_pointer = (page_num * 100) - 100
        end_pointer = start_pointer + 100
    try:
        search_results = paginator.page(page_num)
    except EmptyPage:
        search_results = []
    return render(request,
                  'search/search.html',
                  {'search_query': search_query,
                   'simple_query': search_query,
                   'total_results': total_results,
                   'start_pointer': start_pointer,
                   'end_pointer': end_pointer,
                   'composers': Composer.objects.all().order_by('last_name'),
                   'item_types': ItemType.objects.all().order_by('type_name'),
                   'titles': PieceTitle.objects.all().order_by('name'),
                   'places': Place.objects.all().order_by('place_name'),
                   'search_results': search_results}
                 )

def advanced_search(request):
    if not request.GET.get('keyword-query', None) or request.GET.get('keyword-query', None) != 'none':
        keyword_query = request.GET.get('keyword-query', None)
    else:
        keyword_query = None
    if not request.GET.get('composer-query', None) or request.GET.get('composer-query', None) != 'none':
        composer_query = request.GET.get('composer-query', None)
    else:
        composer_query = None
    if not request.GET.get('dealer-query', None) or request.GET.get('dealer-query', None) != 'none':
        dealer_query = request.GET.get('dealer-query', None)
    else:
        dealer_query = None
    if not request.GET.get('catalog-query', None) or request.GET.get('catalog-query', None) != 'none':
        catalog_query = request.GET.get('catalog-query', None)
    else:
        catalog_query = None
    if not request.GET.get('place-query', None) or request.GET.get('place-query', None) != 'none':
        place_query = request.GET.get('place-query', None)
    else:
        place_query = None
    if not request.GET.get('title-query', None) or request.GET.get('title-query', None) != 'none':
        title_query = request.GET.get('title-query', None)
    else:
        title_query = None
    if not request.GET.get('author-or-responsible-query', None) or request.GET.get('author-or-responsible-query', None) != 'none':
        author_responsible_query = request.GET.get('author-or-responsible-query', None)
    else:
        author_responsible_query = None
    if not request.GET.get('recipient-or-dedicatee-query', None) or request.GET.get('recipient-or-dedicatee-query', None) != 'none':
        recipient_dedicatee_query = request.GET.get('recipient-or-dedicatee-query', None)
    else:
        recipient_dedicatee_query = None
    if not request.GET.get('item-type-query', None) or request.GET.get('item-type-query', None) != 'none':
        item_type_query = request.GET.get('item-type-query', None)
    else:
        item_type_query = None
    if not request.GET.get("start-year-query", None) or request.GET.get('start-year-query', None) != 'none':
        start_year_query = request.GET.get("start-year-query", None)
        print(start_year_query)
    else:
        start_year_query = None
    if not request.GET.get("end-year-query", None) or request.GET.get('start-year-query', None) != 'none':
        end_year_query = request.GET.get("end-year-query", None)
    else:
        end_year_query = None

    search_results = CatalogItemPage.objects.all()
    if composer_query:
        composer = Composer.objects.filter(last_name=composer_query)
        search_results = search_results.filter(item_composer=composer[0])
    if dealer_query:
        dealer = Dealer.objects.filter(the_name__contains=dealer_query)
        search_results = search_results.filter(item_dealer=dealer[0])
    if catalog_query:
        catalog = Catalog.objects.filter(catalog_name=catalog_query)
        search_results = search_results.filter(item_catalog=catalog[0])
    if author_responsible_query:
        author = AuthorOrResponsible.objects.filter(author_name=author_responsible_query)[0]
        authors = AuthorOrResponsibleOrderable.objects.filter(an_author=author)[0]
        search_results = search_results.filter(item_authororesposibles=authors)
    if recipient_dedicatee_query:
        recipient = RecipientOrDedicatee.objects.filter(recipient_name=recipient_dedicatee_query)[0]
        recipients = RecipientOrDedicateeOrderable.objects.filter(a_recipient=recipient)[0]
        search_results = search_results.filter(item_recipientordedicatees=recipients)
    if place_query:
        places = Place.objects.filter(place_name=place_query)[0]
        places = PlaceOrderable.objects.filter(a_place=places)
        search_results = search_results.filter(item_places__in=places)
    if title_query:
        titles = PieceTitle.objects.filter(name__contains=title_query)[0]
        titles = PieceTitleOrderable.objects.filter(a_title=titles)
        search_results = search_results.filter(item_titles__in=titles)
    if item_type_query:
        item_types = ItemType.objects.filter(type_name=item_type_query)[0]
        item_types = ItemTypeOrderable.objects.filter(a_type=item_types)
        search_results = search_results.filter(item_types__in=item_types)
    if keyword_query:
        search_results = search_results.filter(Q(item_description__contains=keyword_query) |\
                                               Q(field_notes__contains=keyword_query) |\
                                               Q(title__contains=keyword_query))
    if start_year_query:
        start_year_query = int(start_year_query)
        search_results = search_results.filter(start_date_year__gt=start_year_query)
        print(search_results.count())
    if end_year_query:
        end_year_query = int(end_year_query)
        print(search_results.count())
        search_results = search_results.filter(end_date_year__lt=end_year_query)
        print(search_results.count())
    search_query = []
    if keyword_query:
        search_query.append("full text=" + keyword_query)
    if composer_query:
        search_query.append("composer=" + composer_query)
    if dealer_query:
        search_query.append("dealer=" + dealer_query)
    if catalog_query:
        search_query.append("catalog=" + catalog_query)
    if place_query:
        search_query.append("place=" + place_query)
    if place_query:
        search_query.append("place=" + place_query)
    if title_query:
        search_query.append("title=" + title_query)
    if item_type_query:
        search_query.append("item type=" + item_type_query)
    if author_responsible_query:
        search_query.append("author or responsible=" + author_responsible_query)
    if recipient_dedicatee_query:
        search_query.append("recipient or dedicatee=" + recipient_dedicatee_query)
    if start_year_query:
        search_query.append("start year=" + str(start_year_query))
    if end_year_query:
        search_query.append("end year=" + str(end_year_query))
    search_query = " and ".join(search_query)
    query = Query.get(search_query)
    query.add_hit()
    total_results = search_results.count()
    page_num = int(request.GET.get("page", 1))
    paginator = Paginator(search_results, 100)
    if page_num == 1:
        start_pointer = 1
        if total_results - ((page_num * 100) - 100) < 100:
            end_pointer = total_results
        else:
            end_pointer = 100
    elif total_results - ((page_num * 100) - 100) < 100:
        start_pointer = (page_num * 100) - 100
        end_pointer = total_results
    else:
        start_pointer = (page_num * 100) - 100
        end_pointer = start_pointer + 100
    try:
        search_results = paginator.page(page_num)
    except EmptyPage:
        search_results = []
    return render(request,
                  'search/search.html',
                  {'search_results': search_results,
                   'search_query': search_query,
                   'total_results': total_results,
                   'page_num': page_num,
                   'start_pointer': start_pointer,
                   'end_pointer': end_pointer,
                   'composer': Composer.objects.all().order_by('last_name'),
                   'item_types': ItemType.objects.all().order_by('type_name'),
                   'titles': PieceTitle.objects.all().order_by('name'),
                   'places': Place.objects.all().order_by('place_name'),
                   'keyword_query': keyword_query,
                   'composer_query': composer_query,
                   'dealer_query': dealer_query,
                   'catalog_query': catalog_query,
                   'place_query': place_query,
                   'title_query': title_query,
                   'start_year_query': start_year_query,
                   'end_year_query': end_year_query,
                   'item_type_query': item_type_query}
                 )

