# coding: utf-8

from django.template import Library

register = Library()


@register.inclusion_tag('cmsplugin_footnote/footnote_list.html',
                        takes_context=True)
def footnote_list(context, placeholder_name, page=None):
    if page is None:
        page = context['request'].current_page
    placeholder = page.placeholders.get(slot=placeholder_name)
    plugins = placeholder.cmsplugin_set.filter(plugin_type='FootnotePlugin') \
                                       .order_by('tree_id', 'rght')
    footnote_plugins = (p.get_plugin_instance()[0] for p in plugins)
    context['footnote_plugins'] = footnote_plugins
    context['placeholder_name'] = placeholder_name
    return context
