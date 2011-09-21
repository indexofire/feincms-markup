# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.conf import settings
from django.http import HttpResponseNotAllowed, HttpResponse
from django.template import TemplateSyntaxError, RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from feincms_markup.forms import MarkupContentAdminForm
from feincms_markup.parsers import MarkupParser


class MarkupContent(models.Model):
    """
    Markup Content Type.
    The class support three markup type: restructuredtext, markdown and
    textile right now.

    Usage:
    add code to your app:
    from feincms.module.page.models import Page
    from feincms_markup.models import MarkupContent

    Page.create_content_type(MarkupContent)
    """
    markup = models.TextField(_("Markup Text"), blank=False)
    markup_type = models.CharField(max_length=20, blank=False,
        choices=MARKUP_CHOICES)
    markup_html = models.TextField(blank=False)
    template = 'feincms_markup/default.html'
    feincms_item_editor_form = MarkupContentAdminForm
    #feincms_item_editor_context_processors = (
    #    lambda x: dict(MARKITUP_JS_URL = settings.MARKITUP_JS_URL),
    #)
    feincms_item_editor_includes = {'head': [ 'feincms_markup/init.html',],}

    class Meta:
        abstract = True
        verbose_name = _('Markup')
        verbose_name_plural = _('Markup')

    @property
    def media(self):
        return forms.Media(css={'all': ('markup/css/markup.css',)}, js=())

    def save(self, *args, **kwargs):
        #self.markup_html = {'rst': lambda x: restructuredtext(x),
        #    'markdown': lambda x: markdown(x),
        #    'textile': lambda x: textile(x),
        #    }[self.markup_type](self.markup)

        self.markup_html = getattr(MarkupParser(),
            self.markup_type)(self.markup)
        return super(MarkupContent, self).save(*args, **kwargs)

    def new_save(self, *args, **kwargs):
        self.markup_html = get_markup_parser(self.markup_type).parser(self.markup)

    def render(self, request, **kwargs):
        context = RequestContext(request, {'content': self,})
        return render_to_string(self.template, context)

    def preview(self, request, **kwargs):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])

        #try:
        #    plugin = MarkupField.objects.get(
        #    pk=request.POST.get('plugin_id'))
        #except MarkupField.DoesNotExist:
        #    plugin = shortcuts.get_object_or_404(pluginmodel.CMSPlugin,
        #    pk=request.POST.get('plugin_id'))
        #placeholder = plugin.placeholder

        #if not placeholder.has_change_permission(request):
        #    raise http.Http404

        #if not request.POST.get('markup'):
        #    return http.HttpResponse('')

        #return HttpResponse(markup.markup_parser(
        #    request.POST.get('text'), request.POST.get('markup'),
        #    template.RequestContext(request, {'object': plugin,
        #        'placeholder': placeholder,}), placeholder))


def get_markup_parser(markup_type):
    parser_class = get_list_of_markup_classes(settings.MARKUP_TYPE_OPTIONS)
    return markup_classes[markup_id]()

import sys
from .settings import MARKUP_TYPE_OPTIONS
def get_markup_parsers(options=MARKUP_TYPE_OPTIONS):
    objects = {}
    for option in options:
        __import__(option)
        module = sys.modules[option]
        objects[module.MarkupParser.name] = module.MarkupParser
    return objects
