from django.shortcuts import render

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.wagtailsearch.models import Query

from catalogitems.models import RecipientOrDedicateeOrderable, RecipientOrDedicatee, CatalogItemPage

# Create your views here.

def default(request, recipient_id):
    recipient = RecipientOrDedicatee.objects.filter(id=recipient_id)[0]
    search_results = RecipientOrDedicateeOrderable.objects.filter(a_recipient=recipient)
    search_results = CatalogItemPage.objects.filter(item_recipientordedicatees__in=search_results).order_by('title')
    query = Query.get(recipient_id)
    query.add_hit()
    paginator = Paginator(search_results, 100)
    page_num = int(request.GET.get("page", 1))
    try:
        search_results = paginator.page(page_num)
    except EmptyPage:
        search_results = []
    return render(request,
                  'authorview/single.html',
                  {'recipient': "{}".format(recipient.recipient_name),
                   'search_results': search_results}
                 )
