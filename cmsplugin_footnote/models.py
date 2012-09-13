# coding: utf-8

from cms.plugins.text.models import AbstractText
from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _


class Footnote(AbstractText):
    symbol = CharField(_('symbol'), max_length=10, blank=True,
                       help_text=_('Overrides the automatic numbering.'))

    class Meta:
        verbose_name = _('Footnote')
        verbose_name_plural = _('Footnotes')
