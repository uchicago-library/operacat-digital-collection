from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.wagtailsearch.models import Query

from catalogitems.models import CatalogItemPage, Catalog

# Create your views here.

def default(request, catalog_id):
    catalog = Catalog.objects.filter(id=catalog_id)[0]
    search_results = CatalogItemPage.objects.filter(item_catalog=catalog).order_by('title')
    query = Query.get(catalog_id)
    query.add_hit()
    paginator = Paginator(search_results, 100)
    page_num = int(request.GET.get("page", 1))
    try:
        search_results = paginator.page(page_num)
    except EmptyPage:
        search_results = []
    return render(request,
                  'catalogview/single.html',
                  {'catalog': "{}".format(catalog.catalog_name),
                   'search_results': search_results}
                 )

