# coding: utf-8

from cms.plugin_pool import plugin_pool
try:
    from cms.plugins.text.cms_plugins import TextPlugin
except ImportError:
    from djangocms_text_ckeditor.cms_plugins import TextPlugin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .models import Footnote
from .utils import get_footnotes_for_page


class FootnotePlugin(TextPlugin):
    model = Footnote
    name = _('Footnote')
    render_template = 'cmsplugin_footnote/footnote_symbol.html'
    text_enabled = True
    admin_preview = False

    def get_editor_widget(self, request, plugins):
        plugins.remove(FootnotePlugin)
        return super(FootnotePlugin, self).get_editor_widget(request, plugins)

    @staticmethod
    def icon_src(self):
        return settings.STATIC_URL + 'icons/footnote_symbol.png'

    def render(self, context, instance, placeholder_name):
        context = super(FootnotePlugin, self).render(context, instance,
                                                     placeholder_name)
        request = context['request']
        page = request.current_page
        footnotes = get_footnotes_for_page(request, page)
        context['counter'] = footnotes.index(instance) + 1
        return context


plugin_pool.register_plugin(FootnotePlugin)
