from django import template
from ..models import PropertyType

register = template.Library()


def format_amount(value):
    return "{:,} AFN".format(value)


register.filter('format_amount', format_amount)


@register.inclusion_tag('property/property_types_list.html')
def property_types():
    return {'property_types': PropertyType.objects.all().order_by('-id')}