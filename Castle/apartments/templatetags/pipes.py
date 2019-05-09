from django import template

register = template.Library()

@register.filter(name='dotSeperator')
def dotSeperator(value):
    return "{:,}".format(value).replace(',', '.')