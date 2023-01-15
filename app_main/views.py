import json

from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.decorators.http import require_POST

from app_cart.cart import Cart
from app_main.models import Product, Category, GeneralData, Banner, Suscriptor, InfoUtil
from gaia import settings


class BaseView(View):
    def get_my_context_data(self, **kwargs):
        cart = Cart(self.request)
        print('products_in_cart', json.dumps(cart.all(), indent=3))
        print('products_in_cart', cart.all())
        c_x_p = len(cart.all())
        print(c_x_p)
        return {
            'icon': settings.BUSINESS_LOGO_PATH,
            'title': settings.BUSINESS_NAME,
            'logo': settings.BUSINESS_NAME_IMG_PATH,
            'banner': settings.BUSINESS_BANNER,
            'business': GeneralData.objects.first() if GeneralData.objects.exists() else {},
            'products_in_cart': cart.all(),
            'total_price': '',
            'infoUtil_list': InfoUtil.objects.all(),
            'all_categories': sorted(Category.objects.filter(product__isnull=False).distinct(),
                                     key=lambda cat: cat.get_prods_count, reverse=True),
            'host': 'http://' + self.request.get_host() + '/'
        }


class StartPage(BaseView, generic.ListView, ):
    template_name = 'startpage.html'
    queryset = Product.objects.filter(is_active=True)
    paginate_by = 10

    def get_queryset(self):
        qs = super(StartPage, self).get_queryset()
        qs = qs.filter(name__icontains=self.request.GET.get('search', ''))
        return qs

    def get_context_data(self, **kwargs):
        context = super(StartPage, self).get_context_data()
        context.update(self.get_my_context_data())
        gnd = GeneralData.objects.first() if GeneralData.objects.exists() else None
        context['products4'] = Product.objects.filter(is_active=True)[:4]
        context['categories'] = sorted(Category.objects.filter(product__isnull=False).distinct(),
                                       key=lambda cat: cat.get_prods_count, reverse=True)[0:4]
        context['products_destacados'] = Product.objects.filter(is_active=True, is_important=True)[0:10]
        context['products_descuento'] = Product.objects.filter(is_active=True, old_price__isnull=False)[0:10]
        context['products_nuevos'] = Product.objects.filter(is_active=True).order_by('-pk')[0:10]
        context['carousel'] = [b.banner.url for b in Banner.objects.filter(gnd=gnd)] if gnd else [
            settings.STATIC_URL / settings.BUSINESS_BANNER]

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
                # data = product.toJSON()
                cart = Cart(request)
                data = {
                    'product': product.toJSON(),
                    "result": "ok",
                    "amount": cart.cart[str(product.id)]['quantity'] if cart.cart.get(str(product.id)) else 0
                }
                print(data)
            else:
                data['error'] = 'Ha ocurrido un error en el servidor.'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
            return JsonResponse(data, )
        return JsonResponse(data, )


class ProductView(StartPage):
    template_name = 'products.html'


class InfoView(generic.ListView, BaseView):
    template_name = 'info.html'
    # queryset = InfoUtil.objects.all()
    model = InfoUtil

    def get_queryset(self):
        qs = super(InfoView, self).get_queryset()
        qs = qs.filter(title__icontains=self.request.GET.get('search', ''))
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update(self.get_my_context_data())
        context['title'] = 'Informaciones'
        return context


class CatalogoView(StartPage):
    template_name = 'catalogo.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update(self.get_my_context_data())
        context['title'] = 'Catálogo'
        return context


@require_POST
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


def delete_suscriptor(request: HttpRequest, *args, **kwargs: dict):
    email = kwargs.get('email')
    print(email)
    susc = Suscriptor.objects.get(email=email)
    susc.delete()
    return redirect(reverse_lazy('index'))
