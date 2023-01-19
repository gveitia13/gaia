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
        print(self.request.get_host())
        if self.request.get_host().__contains__("127.0.0.1") or self.request.get_host().__contains__("localhost"):
            host = 'http://'
        else:
            host = 'https://'

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
            'host': host + self.request.get_host() + '/',
        }


class StartPage(BaseView, generic.ListView, ):
    template_name = 'startpage.html'
    queryset = Product.objects.filter(is_active=True)
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.GET.get('search'):
            qs = qs.filter(name__icontains=self.request.GET.get('search'))
            self.request.session['search'] = self.request.GET.get('search')
            self.request.session['active'] = '2'
        elif 'search' in self.request.session:
            del self.request.session['search']
            del self.request.session['active']
        self.request.session['index_url'] = str(reverse_lazy('index-cup'))
        print(qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super(StartPage, self).get_context_data()
        context.update(self.get_my_context_data())
        gnd = GeneralData.objects.first() if GeneralData.objects.exists() else None

        if 'search' in self.request.session:
            context['search'] = self.request.session['search']
        context['active'] = '1'
        if 'active' in self.request.session:
            context['active'] = self.request.session['active']
        # Sobreescribir abajo
        context['categories'] = sorted(Category.objects.filter(product__isnull=False).distinct(),
                                       key=lambda cat: cat.get_prods_count, reverse=True)[0:4]
        context['products_destacados'] = Product.objects.filter(is_active=True, is_important=True)[0:10]
        context['products_descuento'] = Product.objects.filter(is_active=True, old_price__isnull=False)[0:10]
        context['products_nuevos'] = Product.objects.filter(is_active=True).order_by('-pk')[0:10]

        context['carousel'] = [b.banner.url for b in Banner.objects.filter(gnd=gnd)] if gnd else [
            settings.STATIC_URL / settings.BUSINESS_BANNER]
        # context['index_url'] = self.request.session['index_url']

        return context

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
                if request.path.__contains__('CUP'):
                    tipo_moneda = 'CUP'
                else:
                    tipo_moneda = 'EUR'
                data = {
                    'product': product.toJSON(),
                    "result": "ok",
                    "amount": cart.cart[str(product.id)]['quantity'] if cart.cart.get(str(product.id)) else 0,
                    'tipo_moneda': tipo_moneda
                }
                print(data)
            else:
                data['error'] = 'Ha ocurrido un error en el servidor.'
        except Exception as e:
            print(str(e))
            data['error'] = str(e)
            return JsonResponse(data, )
        return JsonResponse(data, )


class StartPageCUP(StartPage):
    queryset = Product.objects.filter(is_active=True).exclude(moneda='Euro')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['moneda'] = 'CUP'
        context['categories'] = sorted(
            Category.objects.filter(product__isnull=False, product__moneda__in=['CUP', 'Ambas']).distinct(),
            key=lambda cat: cat.get_prods_count, reverse=True)[0:4]
        context['products_destacados'] = Product.objects.filter(is_active=True, is_important=True).exclude(
            moneda='Euro')[0:10]
        context['products_descuento'] = Product.objects.filter(is_active=True, old_price__isnull=False).exclude(
            moneda='Euro')[0:10]
        context['products_nuevos'] = Product.objects.filter(is_active=True).exclude(moneda='Euro').order_by('-pk')[0:10]
        context['all_categories'] = sorted(
            Category.objects.filter(product__isnull=False, product__moneda__in=['CUP', 'Ambas']).distinct(),
            key=lambda cat: cat.get_prods_count, reverse=True)
        cart = Cart(self.request)
        products_in_cart = []
        if cart.all():
            for c in cart.all():
                if Product.objects.get(pk=c['id']).moneda in ['CUP', 'Ambas']:
                    products_in_cart.append(c)
        context['products_in_cart'] = products_in_cart
        context['catalogo_url'] = reverse_lazy('catalogo-cup')
        context['index_url'] = reverse_lazy('index-cup')
        context['tipo_moneda'] = 'CUP'
        # self.request.session['index_url'] = reverse_lazy('index-cup')
        return context


class StartPageEuro(StartPage):
    queryset = Product.objects.filter(is_active=True).exclude(moneda='CUP')
    template_name = 'startpage_euro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['moneda'] = 'Euro'
        context['categories'] = sorted(
            Category.objects.filter(product__isnull=False, product__moneda__in=['Euro', 'Ambas']).distinct(),
            key=lambda cat: cat.get_prods_count, reverse=True)[0:4]
        context['products_destacados'] = Product.objects.filter(is_active=True, is_important=True).exclude(
            moneda='CUP')[0:10]
        context['products_descuento'] = Product.objects.filter(is_active=True, old_price__isnull=False).exclude(
            moneda='CUP')[0:10]
        context['products_nuevos'] = Product.objects.filter(is_active=True).exclude(moneda='CUP').order_by('-pk')[0:10]
        context['all_categories'] = sorted(
            Category.objects.filter(product__isnull=False, product__moneda__in=['Euro', 'Ambas']).distinct(),
            key=lambda cat: cat.get_prods_count, reverse=True)
        cart = Cart(self.request)
        products_in_cart = []
        if cart.all():
            for c in cart.all():
                if Product.objects.get(pk=c['id']).moneda in ['Euro', 'Ambas']:
                    products_in_cart.append(c)
        context['products_in_cart'] = products_in_cart
        context['catalogo_url'] = reverse_lazy('catalogo-euro')
        context['index_url'] = reverse_lazy('index-euro')
        context['is_euro'] = True
        context['tipo_moneda'] = 'EUR'
        # self.request.session['index_url'] = reverse_lazy('index-euro')
        return context


class InfoView(generic.ListView, BaseView):
    template_name = 'info.html'
    model = InfoUtil

    def get_queryset(self):
        qs = super(InfoView, self).get_queryset()
        qs = qs.filter(title__icontains=self.request.GET.get('search', ''))
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context.update(self.get_my_context_data())
        context['title'] = 'Informaciones'
        context['index_url'] = reverse_lazy('index-cup')
        return context


class CatalogoCUPView(StartPageCUP):
    template_name = 'catalogo.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        # context.update(self.get_my_context_data())
        context['title'] = 'Catálogo | Productos CUP'
        context['tipo_moneda'] = 'CUP'
        return context


class CatalogoEuroView(StartPageEuro):
    template_name = 'catalogo_euro.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        # context.update(self.get_my_context_data())
        context['title'] = 'Catálogo | Productos CUP'
        context['tipo_moneda'] = 'EUR'
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
