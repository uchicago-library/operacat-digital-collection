from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.wagtailsearch.models import Query

from catalogitems.models import CatalogItemPage, Composer
# Create your views here.

def default(request, composer_id):
    composer = Composer.objects.filter(id=composer_id)[0]
    search_results = CatalogItemPage.objects.filter(item_composer=composer).order_by('title')
    query = Query.get(composer_id)
    query.add_hit()
    paginator = Paginator(search_results, 100)
    page_num = int(request.GET.get("page", 1))
    try:
        search_results = paginator.page(page_num)
    except EmptyPage:
        search_results = []
    return render(request,
                  'composerview/single.html',
                  {'composer': "{}, {}".format(composer.last_name, composer.first_name),
                   'search_results': search_results}
                 )
