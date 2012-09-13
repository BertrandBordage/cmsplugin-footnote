# coding: utf-8

from django.template import Library
from ..utils import get_footnotes_for_page

register = Library()


@register.inclusion_tag('cmsplugin_footnote/footnote_list.html',
                        takes_context=True)
def footnote_list(context, page=None):
    request = context['request']
    if page is None:
        page = request.current_page
    context['footnotes'] = get_footnotes_for_page(request, page)
    return context
