from django.shortcuts import render
from django.views import generic

from app_main.models import Product, Category
from gaia import settings


class StartPage(generic.TemplateView):
    template_name = 'startpage.html'

    def get_context_data(self, **kwargs):
        context = super(StartPage, self).get_context_data()
        context['icon'] = settings.BUSINESS_LOGO_PATH
        context['title'] = settings.BUSINESS_NAME
        context['products4'] = Product.objects.all()[:4]
        context['categories'] = Category.objects.all()
        return context
