import json

from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt

from app_main.models import Product, Category, GeneralData, Banner, Suscriptor
from gaia import settings


class BaseView(View):
    def get_context_data(self, **kwargs):
        return {
            'icon': settings.BUSINESS_LOGO_PATH,
            'title': settings.BUSINESS_NAME,
            'logo': settings.BUSINESS_NAME_IMG_PATH,
            'banner': settings.BUSINESS_BANNER,
            'business': GeneralData.objects.first() if GeneralData.objects.exists() else {}
        }


class StartPage(BaseView, generic.TemplateView):
    template_name = 'startpage.html'

    def get_context_data(self, **kwargs):
        context = super(StartPage, self).get_context_data()
        gnd = GeneralData.objects.first() if GeneralData.objects.exists() else None
        context['products4'] = Product.objects.filter(is_active=True)[:4]
        context['categories'] = sorted(Category.objects.all(), key=lambda cat: cat.get_prods_count, reverse=True)[0:4]
        context['all_categories'] = Category.objects.all()
        context['products_destacados'] = Product.objects.filter(is_active=True, is_important=True)[0:10]
        context['products_descuento'] = Product.objects.filter(is_active=True, old_price__isnull=False)[0:10]
        context['products_nuevos'] = Product.objects.filter(is_active=True).order_by('-pk')[0:10]
        context['carousel'] = [b.banner.url for b in Banner.objects.filter(gnd=gnd)] if gnd else [
            settings.STATIC_URL / settings.BUSINESS_BANNER]
        context['first'] = Product.objects.last()
        return context

    # @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict):
        data = {}
        print(request.body)
        try:
            body = json.loads(request.body)
            action = body['action']
            if action == 'details':
                product = Product.objects.get(pk=body['pk'])
                data = product.toJSON()
                print(data)
            else:
                data['error'] = 'Ha ocurrido un error en el servidor.'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
            return JsonResponse(data, )
        return JsonResponse(data, )


def create_suscriptor(request: HttpRequest, *args, **kwargs: dict):
    data = {}
    body = json.loads(request.body)
    try:
        suscriptor = Suscriptor(email=body['email'])
        suscriptor.save()
        data = model_to_dict(suscriptor)
        data['url'] = request.path
    except Exception as e:
        data['error'] = f'Ya existe un suscriptor con el correo {body["email"]}'
    return JsonResponse(data=data, safe=False)
