from django.shortcuts import render
from django.views import generic

from app_main.models import Product, Category, GeneralData
from gaia import settings


class StartPage(generic.TemplateView):
    template_name = 'startpage.html'

    def get_context_data(self, **kwargs):
        context = super(StartPage, self).get_context_data()
        context['icon'] = settings.BUSINESS_LOGO_PATH
        context['title'] = settings.BUSINESS_NAME
        context['logo'] = settings.BUSINESS_NAME_IMG_PATH
        context['banner'] = settings.BUSINESS_BANNER
        context['business'] = GeneralData.objects.first() if GeneralData.objects.exists() else {}
        context['products4'] = Product.objects.filter(is_active=True)[:4]
        context['categories'] = sorted(Category.objects.all(), key=lambda cat: cat.get_prods_count, reverse=True)[0:4]
        context['all_categories'] = Category.objects.all()
        context['products_destacados'] = Product.objects.filter(is_active=True, is_important=True)[0:5]
        context['products_descuento'] = Product.objects.filter(is_active=True, old_price__isnull=False)[0:5]
        context['products_nuevos'] = Product.objects.filter(is_active=True).order_by('-pk')[0:5]
        return context
