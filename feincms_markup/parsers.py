# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import TemplateSyntaxError
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe


class MarkupParser(object):
    """
    Create a markup parser object
    """
    def __init__(self, parser=None):
        self.parser = parser

    def rst(self, value):
        """
        parse restructured text
        """
        try:
            from docutils.core import publish_parts
            from docutils.parsers.rst import directives, Directive
            #from contrib.content.markup.directives.code import CodeHighlight
        except ImportError:
            if settings.DEBUG:
                raise TemplateSyntaxError("Error in content type: The python "
                    "docutils library isn't installed.")
            return force_unicode(value)
        else:
            #if settings.MARKUP_CODE_HIGHTLIGHT:
            #    directives.register_directive('code', CodeHighlight)
            docutils_settings = getattr(settings,
                'RESTRUCTUREDTEXT_FILTER_SETTINGS', {},)
            parts = publish_parts(source=smart_str(value),
                writer_name="html4css1", settings_overrides=docutils_settings,)
            return mark_safe(force_unicode(parts["html_body"]))

    def markdown(self, value):
        """
        Runs Markdown over a given value, optionally using various
        extensions python-markdown supports.

        Syntax::

            {{ value|markdown2:"extension1_name,extension2_name..." }}

        To enable safe mode, which strips raw HTML and only returns HTML
        generated by actual Markdown syntax, pass "safe" as the first
        extension in the list.

        If the version of Markdown in use does not support extensions,
        they will be silently ignored.

        """
        try:
            import markdown
        except ImportError:
            if settings.DEBUG:
                raise TemplateSyntaxError("Error in content type: The python "
                    "markdown library isn't installed.")
            return force_unicode(value)
        else:
            def parse_extra(extra):
                if ':' not in extra:
                    return (extra, {})
                name, values = extra.split(':', 1)
                values = dict((str(val.strip()), True) for val in
                    values.split('|'))
                return (name.strip(), values)
            extensions = ['']
            if settings.MARKUP_CODE_HIGHTLIGHT:
                extensions =['codehilite(force_linenos=True)']
            #extras = (e.strip() for e in arg.split(','))
            #extras = dict(parse_extra(e) for e in extras if e)
            #if 'safe' in extras:
            #    del extras['safe']
            #    safe_mode = True
            #else:
            #    safe_mode = False
            return mark_safe(markdown.markdown(force_unicode(value),
                extensions))

    def textile(self, value):
        """
        parse textile text
        """
        try:
            import textile
        except ImportError:
            if settings.DEBUG:
                raise TemplateSyntaxError("Error in content type: The python "
                    "textile library isn't installed.")
            return force_unicode(value)
        else:
            return mark_safe(force_unicode(textile.textile(smart_str(value),
                encoding='utf-8', output='utf-8')))
