# coding: utf-8

try:
    from cms.plugins.text.models import Text
    from cms.plugins.text.utils import plugin_tags_to_id_list
except ImportError:
    from djangocms_text_ckeditor.models import Text
    from djangocms_text_ckeditor.utils import plugin_tags_to_id_list

from cms.utils.moderator import get_cmsplugin_queryset
from .models import Footnote
from .settings import CMSPLUGIN_FOOTNOTE_DEBUG


def get_footnotes_for_page(request, page):
    """
    Gets the Footnote instances for `page`, with the correct order.
    """
    plugins = get_cmsplugin_queryset(request)
    footnote_and_text_plugins = plugins.filter(
        placeholder__page=page,
        plugin_type__in=('FootnotePlugin', 'TextPlugin'),
    ).order_by('position').values('parent', 'plugin_type', 'pk')

    pks = [p['pk'] for p in footnote_and_text_plugins]
    footnote_dict = {f.cmsplugin_ptr_id: f for f in
                     Footnote.objects.filter(cmsplugin_ptr_id__in=pks)}
    text_dict = {t.cmsplugin_ptr_id: t for t in
                 Text.objects.filter(cmsplugin_ptr_id__in=pks)}

    def get_footnote_or_text(plugin_pk, plugin_type):
        d = footnote_dict if plugin_type == 'FootnotePlugin' else text_dict
        try:
            return d[plugin_pk]
        except KeyError:
            if CMSPLUGIN_FOOTNOTE_DEBUG:
                raise

    root_footnote_and_text_plugins = [p for p in footnote_and_text_plugins
                                      if p['parent'] is None]

    footnotes = []
    for plugin in root_footnote_and_text_plugins:
        footnote_or_text = get_footnote_or_text(plugin['pk'],
                                                plugin['plugin_type'])
        if footnote_or_text is None:
            continue
        if plugin['plugin_type'] == 'FootnotePlugin':
            footnotes.append(footnote_or_text)
        else:
            for pk in plugin_tags_to_id_list(footnote_or_text.body):
                footnote = get_footnote_or_text(pk, 'FootnotePlugin')
                if footnote is not None:
                    footnotes.append(footnote)
    return footnotes
