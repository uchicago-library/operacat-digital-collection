from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.wagtailsearch.models import Query

from catalogitems.models import ItemTypeOrderable, ItemType, CatalogItemPage
# Create your views here.


def default(request, type_id):
    itemtype = ItemType.objects.filter(id=type_id)[0]
    search_results = ItemTypeOrderable.objects.filter(a_type=itemtype)
    search_results = CatalogItemPage.objects.filter(item_types__in=search_results).order_by('title')
    query = Query.get(type_id)
    query.add_hit()
    paginator = Paginator(search_results, 100)
    page_num = int(request.GET.get("page", 1))
    try:
        search_results = paginator.page(page_num)
    except EmptyPage:
        search_results = []
    return render(request,
                  'itemtypeview/single.html',
                  {'itemtype': "{}".format(itemtype.type_name),
                   'search_results': search_results}
                 )
