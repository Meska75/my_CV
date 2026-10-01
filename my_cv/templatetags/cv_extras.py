from django import template

from my_cv.i18n import t as translate

register = template.Library()


@register.simple_tag(name='t')
def t_tag(key):
    return translate(key)


@register.simple_tag
def loc(obj, field):
    if obj is None:
        return ''
    if hasattr(obj, 'loc'):
        return obj.loc(field)
    return getattr(obj, field, '') or ''
