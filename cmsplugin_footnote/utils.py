# coding: utf-8
from cms.models import CMSPlugin
from cms.plugins.text.models import Text

from cms.utils.moderator import get_cmsplugin_queryset
from cms.plugins.text.utils import plugin_tags_to_id_list
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
    root_footnote_and_text_plugins = [p for p in footnote_and_text_plugins if p['parent'] is None]
    pks = [p['pk'] for p in footnote_and_text_plugins]
    footnote_dict = {f.cmsplugin_ptr_id: f for f in Footnote.objects.filter(cmsplugin_ptr_id__in=pks)}
    text_dict = {t.cmsplugin_ptr_id: t for t in Text.objects.filter(cmsplugin_ptr_id__in=pks)}
    footnotes = []
    for plugin in root_footnote_and_text_plugins:
        if plugin['plugin_type'] == 'FootnotePlugin':
            footnotes.append(footnote_dict[plugin['pk']])
        else:
            for pk in plugin_tags_to_id_list(text_dict[plugin['pk']].body):
                try:
                    footnotes.append(footnote_dict[pk])
                except KeyError:
                    if CMSPLUGIN_FOOTNOTE_DEBUG:
                        raise
    return footnotes
