from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.wagtailsearch.models import Query

from catalogitems.models import PlaceOrderable, Place, CatalogItemPage
# Create your views here.

def default(request, place_id):
    place = Place.objects.filter(id=place_id)[0]
    search_results = PlaceOrderable.objects.filter(a_place=place)
    search_results = CatalogItemPage.objects.filter(item_places__in=search_results).order_by('title')
    query = Query.get(place_id)
    query.add_hit()
    paginator = Paginator(search_results, 100)
    page_num = int(request.GET.get("page", 1))
    try:
        search_results = paginator.page(page_num)
    except EmptyPage:
        search_results = []
    return render(request,
                  'placeview/single.html',
                  {'place': "{}".format(place.place_name),
                   'search_results': search_results}
                 )
