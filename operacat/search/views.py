from __future__ import absolute_import, unicode_literals

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from sys import stderr

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query
from wagtail.wagtailsearch.backends import get_search_backend

from catalogitems.models import *

def search(request):
    search_query = request.GET.get.get('query', None)
    if search_query:
        search_results = CatalogItemPage.objects.order_by('title').live().search(search_query)
        query = Query.get(search_query)
        query.add_hit()
    else:
        search_results = CatalogItemPage.objects.none()
    paginator = Paginator(search_results, 100)
    page_num = int(request.GET.get.get("page", 1))
    try:
        search_results = paginator.page(page_num)
    except EmptyPage:
        search_results = []
    return render(request,
                  'search/search.html',
                  {'search_query': search_query,
                   'search_results': search_results}

                 )


def advanced_search(request):
    if not request.GET.get('composer-query', None) or request.GET.get('composer-query', None) != '---':
        composer_query = request.GET.get('composer-query', None)
    if not request.GET.get('dealer-query', None) or request.GET.get('dealer-query', None) != '---':
        dealer_query = request.GET.get('dealer-query', None)
    else:
        dealer_query = None
    if not request.GET.get('catalog-query', None) or request.GET.get('catalog-query', None) != '---':
        catalog_query = request.GET.get('catalog-query', None)
    else:
        catalog_query = None
    if not request.GET.get('place-query', None) or request.GET.get('place-query', None) != '---':
        place_query = request.GET.get('place-query', None)
    else:
        place_query = None
    if not request.GET.get('title-query', None) or request.GET.get('title-query', None) != '---':
        title_query = request.GET.get('title-query', None)
    else:
        title_query = None
    if not request.GET.get('item-type-query', None) or request.GET.get('item-type-query', None) != '---':
        item_type_query = request.GET.get('item-type-query', None)
    else:
        item_type_query = None
    page_num = int(request.GET.get("page", 1))
    search_results = CatalogItemPage.objects.all()
    if composer_query:
        composer = Composer.objects.filter(last_name=composer_query)
        search_results = search_results.filter(item_composer=composer[0])
    if dealer_query:
        dealer = Dealer.objects.filter(dealer_name=dealer_query)
        search_results = search_results.filter(item_dealer=dealer[0])
    if catalog_query:
        catalog = Catalog.objects.filter(catalog_name=catalog_query)
        search_results = search_results.filter(item_catalog=catalog[0])
    if place_query:
        places = Place.objects.filter(place_name=place_query)[0]
        places = PlaceOrderable.objects.filter(a_place=places)[0]
        search_results = search_results.filter(item_places=composer)
    if title_query:
        titles = PieceTitle.objects.filter(name__contains=title_query)[0]
        titles = PieceTitleOrderable.objects.filter(a_title=titles)[0]
        search_results = search_results.filter(item_titles=titles)
    if item_type_query:
        item_types = ItemType.objects.filter(type_name=item_type_query)[0]
        item_types = ItemTypeOrderable.objects.filter(a_type=item_types)[0]
        search_results = search_results.filter(item_types=item_types)
    search_query = "{},{},{},{},{},{}".format(composer_query, dealer_query, catalog_query, place_query, title_query, item_type_query)
    query = Query.get(search_query)
    query.add_hit()
    paginator = Paginator(search_results, 100)
    try:
        search_results = paginator.page(page_num)
    except EmptyPage:
        search_results = []
    return render(request,
                  'search/search.html',
                  {'search_results': search_results,
                   'composer_query': composer_query,
                   'dealer_query': dealer_query,
                   'catalog_query': catalog_query,
                   'place_query': place_query,
                   'title_query': title_query,
                   'item_type_query': item_type_query}
                 )


