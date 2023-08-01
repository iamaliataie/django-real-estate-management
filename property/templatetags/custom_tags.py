from django import template

register = template.Library()


def format_amount(value):
    return "$ {:,.2f}".format(value)


register.filter('format_amount', format_amount)