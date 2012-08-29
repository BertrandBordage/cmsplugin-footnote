# coding: utf-8

from cms.plugins.text.cms_plugins import TextPlugin
from .models import Footnote
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .utils import get_footnote_plugins
from cms.plugin_pool import plugin_pool


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
        page = context['request'].current_page
        footnote_plugins = get_footnote_plugins(page, placeholder_name)
        context['counter'] = footnote_plugins.index(instance) + 1
        context['placeholder_name'] = placeholder_name
        return context


plugin_pool.register_plugin(FootnotePlugin)
