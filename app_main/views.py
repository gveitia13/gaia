from django.shortcuts import render
from django.views import generic

from gaia import settings


class StartPage(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(StartPage, self).get_context_data()
        context['icon'] = settings.BUSINESS_LOGO_PATH
        context['title'] = settings.BUSINESS_NAME
        return context
