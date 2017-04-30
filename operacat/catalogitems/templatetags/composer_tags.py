
from django import template
from catalogitems.models import Composer

register = template.Library()

@register.inclusion_tag("catalogitems/tags/composer_tags.html", takes_context=True)
def composers(context):
    return {
        'composers': Composer.objects.all(),
        'request': context['request']
    }
