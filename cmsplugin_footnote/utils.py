from django.core.cache import cache


def get_cache_key(page, placeholder_name):
        return 'footnote_plugins_%d_%s' % (page.pk, placeholder_name)


def get_footnote_plugins(page, placeholder_name):
    cache_key = get_cache_key(page, placeholder_name)
    footnote_plugins = cache.get(cache_key)
    if footnote_plugins is None:
        placeholder = page.placeholders.get(slot=placeholder_name)
        plugins = placeholder.cmsplugin_set \
                             .filter(plugin_type='FootnotePlugin') \
                             .order_by('tree_id', 'rght')
        footnote_plugins = [p.get_plugin_instance()[0] for p in plugins]
        cache.set(cache_key, footnote_plugins)
    return footnote_plugins
