from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.wagtailsearch.models import Query

from catalogitems.models import CatalogItemPage, Dealer

def search_by_keyword(request):
    the_query = request.GET["query"]
    print(the_query)
    dealers = Dealer.objects.filter(dealer_name__contains=the_query)
    print(dealers)
    search_results = CatalogItemPage.objects.filter(item_dealer__in=dealers).order_by('title')
    print(search_results)
    query = Query.get(the_query)
    query.add_hit()
    paginator = Paginator(search_results, 100)
    page_num = int(request.GET.get("page", 1))
    try:
        search_results = paginator.page(page_num)
    except EmptyPage:
        search_results = []
    return render(request,
                  'dealerview/single.html',
                  {'dealer': "{}".format(the_query),
                   'query': the_query,
                   'search_results': search_results}
                 )

def browse(request):
    items = Dealer.objects.all().order_by('dealer_name')
    return render(request,
                  "dealerview/browse.html",
                  {'results':items}
                 )
