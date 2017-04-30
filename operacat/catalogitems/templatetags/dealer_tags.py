
from django import template
from catalogitems.models import Dealer

register = template.Library()

@register.inclusion_tag("catalogitems/tags/dealer_tags.html", takes_context=True)
def dealers(context):
    return {
        'dealers': Dealer.objects.all()[0:5],
        'request': context['request']
    }
