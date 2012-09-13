# coding: utf-8

from django.conf import settings


CMSPLUGIN_FOOTNOTE_DEBUG = getattr(settings, 'CMSPLUGIN_FOOTNOTE_DEBUG',
                                   False)
