# -*- coding: utf-8 -*-
from django.conf import settings


if hasattr(settings, 'FEINCMS_MARKUP_TYPES'):
    MARKUP_TYPE_OPTIONS = settings.FEINCMS_MARKUP_TYPES
else:
    MARKUP_TYPE_OPTIONS = (
        'feincms_markup.parsers.restructuredtext',
        'feincms_markup.parsers.markdown',
        'feincms_markup.parsers.textile',
    )
