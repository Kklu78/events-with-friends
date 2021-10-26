from django import template

register = template.Library()

@register.filter(name='getkey')
def getkey(d, k):
    return d.get(k, None)