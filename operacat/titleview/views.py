from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.wagtailsearch.models import Query

from catalogitems.models import PieceTitleOrderable, PieceTitle, CatalogItemPage
# Create your views here.


def default(request, title_id):
    title = PieceTitle.objects.filter(id=title_id)[0]
    search_results = PieceTitleOrderable.objects.filter(a_title=title)
    search_results = CatalogItemPage.objects.filter(item_titles__in=search_results).order_by('title')
    query = Query.get(title_id)
    query.add_hit()
    paginator = Paginator(search_results, 100)
    page_num = int(request.GET.get("page", 1))
    try:
        search_results = paginator.page(page_num)
    except EmptyPage:
        search_results = []
    return render(request,
                  'titleview/single.html',
                  {'title': "{}".format(title.name),
                   'search_results': search_results}
                 )
