from django import template

register = template.Library()


def format_amount(value):
    return "{:,} AFN".format(value)


register.filter('format_amount', format_amount)