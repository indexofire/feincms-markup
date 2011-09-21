# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe


class MarkupBaseParser(object):
    def parse(self, value):
        return mark_safe(value)

