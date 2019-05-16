from django import template

register = template.Library()

@register.filter(name='dotSeperator')
def dotSeperator(value):
    return "{:,}".format(value).replace(',', '.')

@register.filter(name='roomFixer')
def roomFixer(value):
    if value == '6' or value == 6:
        return '6+'
    return value