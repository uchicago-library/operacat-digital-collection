"""this is the definition for composer tags for the site

This is what enables the dynamically generated list of composers on
the homepage of the site.
"""

from catalogitems.models import Composer
from django import template


register = template.Library()


@register.inclusion_tag("catalogitems/tags/composer_tags.html",
                        takes_context=True)
def composers(context):
    """a method to return a JSON object to iterate through in a html template

    returns a dict with two keys:
    - composers is a list of Composer objects,
    - request is an http request object from current session request
    """
    return {
        'composers': Composer.objects.all(),
        'request': context['request']
    }
