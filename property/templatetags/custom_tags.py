from django import template
from ..models import PropertyType
from search.models import SearchCriteria

register = template.Library()


def format_amount(value):
    return "{:,} AFN".format(value)
register.filter('format_amount', format_amount)


@register.inclusion_tag('property/property_types_list.html')
def property_types():
    return {'property_types': PropertyType.objects.all()}


@register.inclusion_tag('search/search_criteria.html', takes_context=True)
def search_criteria(context):
    user = context.get('user')
    if user.is_authenticated:
        search = SearchCriteria.objects.filter(user=user).last()
    else:
        search = None
    return {'search': search.get_search_criteria() if search else False } 