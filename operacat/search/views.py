from __future__ import absolute_import, unicode_literals

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render

from sys import stderr

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query
from wagtail.wagtailsearch.backends import get_search_backend

from catalogitems.models import CatalogItemPage, Composer, Dealer, Catalog

def search(request):
    search_query = request.GET.get('query', None)
    if search_query:
        search_results = CatalogItemPage.objects.order_by('title').live().search(search_query)
        query = Query.get(search_query)
        query.add_hit()
    else:
        search_results = CatalogItemPage.objects.none()
    paginator = Paginator(search_results, 100)
    page_num = int(request.GET.get("page", 1))
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
    composer_query = request.GET.get('composer-query', None) if request.GET.get('composer-query', None) != 'none' else None
    dealer_query = request.GET.get('dealer-query', None) if request.GET.get('dealer-query', None) != 'none' else None
    catalog_query = request.GET.get('catalog-query', None) if request.GET.get('catalog-query', None) != 'none' else None
    page = request.GET.get('page', 1)
    search_results = CatalogItemPage.objects
    if composer_query and composer_query != "---":
        composer = Composer.objects.filter(last_name=composer_query)[0]
        search_results = search_results.filter(item_composer=composer)
    elif dealer_query and dealer_query != "---":
        dealer = Dealer.objects.filter(dealer_name=dealer_query)[0]
        search_results.filter(item_dealer=dealer)
    elif catalog_query and catalog_query != "---":
        catalog = Catalog.objects.filter(dealer_name=catalog_query)[0]
        search_results.filter(item_catalog=catalog)
    if search_results.count() > 0:
        search_results = search_results
    else:
        search_results = CatalogItemPage.objects.none()
    paginator = Paginator(search_results, 100)
    page_num = int(request.GET.get("page", 1))
    try:
        search_results = paginator.page(page_num)
    except EmptyPage:
        search_results = []
    return render(request,
                  "search/search.html",
                  {
                   'search_results': search_results}
                 )

