# coding: utf-8

from django.core.cache import cache
from cms.utils.moderator import get_cmsplugin_queryset
from cms.plugins.text.utils import plugin_tags_to_id_list
from cms.plugins.utils import downcast_plugins
from cms.models import CMSPlugin
from .settings import CMSPLUGIN_FOOTNOTE_DEBUG


def get_cache_key(page, plugins):
    return 'footnote_plugins__%d_%d' \
            % (page.pk, plugins.filter(placeholder__page=page,
                                       plugin_type='FootnotePlugin').count())


def delete_cache_key(page):
    plugins = CMSPlugin.objects.all()
    cache_key = get_cache_key(page, plugins)
    cache.delete(cache_key)


def plugin_is_footnote(plugin):
    return plugin.plugin_type == 'FootnotePlugin'


def plugin_iterator_from_text_plugin(text_plugin):
    plugin_pk_list = plugin_tags_to_id_list(text_plugin.body)
    for pk in plugin_pk_list:
        try:
            yield CMSPlugin.objects.get(pk=pk)
        except CMSPlugin.DoesNotExist, e:
            if CMSPLUGIN_FOOTNOTE_DEBUG:
                raise e


def get_footnotes_for_page(request, page):
    '''
    Gets the Footnote instances for `page`, with the correct order.
    '''
    plugins = get_cmsplugin_queryset(request)
    cache_key = get_cache_key(page, plugins)
    footnotes = cache.get(cache_key)
    if footnotes is None:
        root_footnote_and_text_plugins = plugins.filter(
                placeholder__page=page,
                plugin_type__in=('FootnotePlugin', 'TextPlugin'),
                parent=None
            ).order_by('position')
        footnote_plugins = []
        footnote_plugins__append = footnote_plugins.append
        for p in root_footnote_and_text_plugins:
            if plugin_is_footnote(p):
                footnote_plugins__append(p)
            else:
                text = downcast_plugins((p,))[0]
                plugin_iterator = plugin_iterator_from_text_plugin(text)
                for plugin in plugin_iterator:
                    if plugin_is_footnote(plugin):
                        footnote_plugins__append(plugin)
        footnotes = downcast_plugins(footnote_plugins)
        cache.set(cache_key, footnotes)
    return footnotes
