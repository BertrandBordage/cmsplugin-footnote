from cms.plugins.text.models import AbstractText
from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatewords_html
from django.utils.html import strip_tags
from .utils import get_cache_key
from django.core.cache import cache


class Footnote(AbstractText):
    symbol = CharField(_('symbol'), max_length=10, blank=True,
                       help_text=_('Overrides the automatic numbering.'))

    class Meta:
        verbose_name = _('Footnote')
        verbose_name_plural = _('Footnotes')

    def __unicode__(self):
        return strip_tags(truncatewords_html(self.body, 5))

    def save(self, *args, **kwargs):
        super(Footnote, self).save(*args, **kwargs)
        placeholder, page = self.placeholder, self.placeholder.page
        cache_key = get_cache_key(page, placeholder.slot)
        cache.delete(cache_key)
