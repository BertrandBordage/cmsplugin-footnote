# coding: utf-8

from django.template import Library
from ..utils import get_footnote_plugins

register = Library()


@register.inclusion_tag('cmsplugin_footnote/footnote_list.html',
                        takes_context=True)
def footnote_list(context, placeholder_name, page=None):
    if page is None:
        page = context['request'].current_page
    context['footnote_plugins'] = get_footnote_plugins(page, placeholder_name)
    context['placeholder_name'] = placeholder_name
    return context
