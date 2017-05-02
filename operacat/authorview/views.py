from django.shortcuts import render

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.wagtailsearch.models import Query

from catalogitems.models import AuthorOrResponsibleOrderable, AuthorOrResponsible, CatalogItemPage

# Create your views here.

def default(request, author_id):
    author = AuthorOrResponsible.objects.filter(id=author_id)[0]
    search_results = AuthorOrResponsibleOrderable.objects.filter(an_author=author)
    search_results = CatalogItemPage.objects.filter(item_authororesposibles__in=search_results).order_by('title')
    query = Query.get(author_id)
    query.add_hit()
    paginator = Paginator(search_results, 100)
    page_num = int(request.GET.get("page", 1))
    try:
        search_results = paginator.page(page_num)
    except EmptyPage:
        search_results = []
    return render(request,
                  'authorview/single.html',
                  {'author': "{}".format(author.author_name),
                   'search_results': search_results}
                 )
