"""the views functions for the dealerview application

This allows the inclusion of urls that will query for a list of all
dealers in the system
"""

from django.shortcuts import render

from catalogitems.models import CatalogItemPage, Dealer

def browse(request):
    """a function to return an html formatted web request with a list of all dealers in the system

    It queries the dtabase for all dealers ordered by name in the default descending order. Then it
    returns a web request object of formatted html with that list as data labeled 'results'

    """
    items = Dealer.objects.all()
    whole_list = []
    for n_item in items:
        whole_list.append(n_item)
    final_result = sorted(whole_list,
                          key=lambda x: (x.common_name.common_name_text, x.the_name))
    return render(request,
                  "dealerview/browse.html",
                  {'results':final_result}
                 )
