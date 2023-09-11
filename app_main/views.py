import datetime
import http.client
import json
import os
import random
import re
from hashlib import sha256, sha1
from django.core.cache import cache
import pytz
from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import generics

from app_cart.cart import Cart
from app_main.models import Product, Category, GeneralData, Banner, Suscriptor, InfoUtil, Municipio, Orden, \
    ComponenteOrden
from app_main.serializers import OrdenSerializer
from gaia import settings


class BaseView(View):

    def get_my_context_data(self, **kwargs):
        cart = Cart(self.request)
        c_x_p = len(cart.all())
        if self.request.get_host().__contains__("127.0.0.1") or self.request.get_host().__contains__(
                "localhost"):
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
            'infoUtil_list': InfoUtil.objects.filter(title__isnull=False)[:4],
            'all_categories': sorted(Category.objects.filter(product__isnull=False).distinct(),
                                     key=lambda cat: cat.get_prods_count, reverse=True),
            'host': host + self.request.get_host() + '/' if settings.TECHNOSTAR else 'https://gaia-mercado.com/',
            # 'host': host + self.request.get_host() + '/' if settings.TECHNOSTAR else 'http://185.101.227.197:8080/',
            'address': Municipio.objects.filter(visible=True)
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
        return qs

    def get_context_data(self, **kwargs):
        context = super(StartPage, self).get_context_data()
        context.update(self.get_my_context_data())
        gnd = GeneralData.objects.first() if GeneralData.objects.exists() else None
        if gnd is not None:
            context['meta_tittle'] = gnd.meta_tittle
            context['meta_desc'] = gnd.meta_description
            context['meta_kw'] = gnd.meta_kw
        if 'search' in self.request.session:
            context['search'] = self.request.session['search']
        context['active'] = '1'
        if 'active' in self.request.session:
            context['active'] = self.request.session['active']
        # Sobreescribir abajo
        context['categories'] = sorted(
            Category.objects.filter(product__isnull=False, product__is_active=True, destacado=True).distinct(),
            key=lambda cat: cat.get_prods_count, reverse=True)[0:4]
        context['products_destacados'] = Product.objects.filter(is_active=True, is_important=True)[0:10]
        context['products_descuento'] = Product.objects.filter(is_active=True, old_price__isnull=False)[0:10]
        context['products_nuevos'] = Product.objects.filter(is_active=True).order_by('-pk')[0:10]
        context['carousel'] = [b.banner.url for b in Banner.objects.filter(gnd=gnd)] if gnd else [
            os.path.join(settings.STATIC_URL, settings.BUSINESS_BANNER)]
        return context

    def dispatch(self, request, *args, **kwargs):
        self.request.session['active_cart'] = None
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: list, **kwargs: dict):
        data = {}
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
            else:
                data['error'] = 'Ha ocurrido un error en el servidor.'
        except Exception as e:
            data['error'] = str(e)
            return JsonResponse(data, )
        return JsonResponse(data, )


class StartPageCUP(StartPage):

    def dispatch(self, request, *args, **kwargs):
        return redirect('https://gaia-mercado.com')


class StartPageEuro(StartPage):
    pass

def info_redirect(request):
    return redirect(request)

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
        cate = sorted(
            Category.objects.filter(product__isnull=False, destacado=True,
                                    product__moneda__in=['CUP', 'Ambas']).distinct(),
            key=lambda cat: cat.get_prods_count, reverse=True)
        if len(cate) > 4:
            context['categories'] = random.sample(cate, 4)
        else:
            context['categories'] = random.sample(cate, len(cate))
        context['catalogo_url'] = reverse_lazy('catalogo-cup')
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
        context['title'] = 'Catálogo | Productos CUP'
        context['tipo_moneda'] = 'EUR'
        context['is_euro'] = True
        return context


@require_POST
@method_decorator(csrf_exempt)
def create_suscriptor(request: HttpRequest, *args, **kwargs: dict):
    data = {}
    body = json.loads(request.body)
    email = body['email']
    try:
        # Parse the request body as JSON
        suscriptor = Suscriptor(email=email)
        suscriptor.save()
        data = model_to_dict(suscriptor)
        data['url'] = request.path
    except Exception:
        data['error'] = f'Ya existe un suscriptor con el correo {email}'
    return JsonResponse(data=data, safe=False)


def delete_suscriptor(request: HttpRequest, *args, **kwargs: dict):
    email = kwargs.get('email')
    susc = Suscriptor.objects.get(email=email)
    susc.delete()
    return redirect(reverse_lazy('index'))


@csrf_exempt
def pagar_euro(request):
    if request.method == 'POST':
        if GeneralData.objects.all()[0].checkout_allowed == True:
            purchase_data = json.loads(request.body.decode('utf-8'))
            purchase_data['cart_id'] = request.headers.get('X-Session-ID')
            orden = create_order(purchase_data, 'Euro', **{})
            if orden:
                mensaje = create_message_order(request, orden)
                conn = http.client.HTTPSConnection("" + settings.TPP_URL + "")
                # genera un request json
                payload_tpp = {"grant_type": "client_credentials", "client_id": settings.TPP_CLIENT_ID,
                               "client_secret": settings.TPP_CLIENT_SECRET}
                # hago la petition y capturo el response
                payload_tpp = json.dumps(payload_tpp)
                headers = {'Content-Type': "application/json"}
                # se hace el post
                conn.request("POST", "/api/v2/access/token", payload_tpp, headers)
                res = conn.getresponse()
                data = res.read()
                token = data.decode("utf-8")
                token = json.loads(token)['access_token']
                user_comprador = orden.nombre_comprador
                # Convertir total a 2 decimales
                address = 'Reparto: ' + orden.municipio + '. '
                address += 'Calle: ' + orden.calle + '. '
                address += 'Entre calle : ' + orden.calle1 + ' y calle ' + orden.calle2 + '. '
                address += 'Número: ' + orden.numero_edificio + '. '
                # if orden.reparto != '':
                #     address += 'Reparto: ' + orden.reparto + '. '
                if orden.detalles_direccion != '':
                    address += 'Detalles : ' + orden.detalles_direccion + '.'
                client = {
                    'name': user_comprador.split(' ')[0],
                    'lastName': ''.join(a + ' ' for a in [i for i in user_comprador.split(' ')[1:]]) if len(
                        user_comprador.split(' ')) > 1 else ' ',
                    "address": address,
                    "phone": orden.telefono_comprador,
                    "email": orden.correo,
                    "countryId": 0,
                    "termsAndConditions": "true"
                }
                impuesto = orden.total * GeneralData.objects.first().tropipay_impuesto / 100
                if impuesto > 0:
                    orden_total = round((orden.total + impuesto + 0.5), 2) * 100
                else:
                    orden_total = round((orden.total), 2) * 100
                spain_timezone = pytz.timezone("Europe/Madrid")
                spain_time = datetime.datetime.now(spain_timezone)
                payload_tpp = {
                    "reference": str(orden.uuid),
                    "concept": "Orden de GAIA a nombre de " + client['email'],
                    "favorite": "false",
                    "description": mensaje,
                    "amount": orden_total,  # para quitar decimales
                    "currency": 'EUR',
                    "singleUse": "true",
                    "reasonId": 4,
                    "expirationDays": 0,
                    "lang": "es",
                    "urlSuccess": "" + settings.TPP_SUCCESS_URL + "",
                    "urlFailed": "" + settings.TPP_FAILED_URL + "",
                    "urlNotification": "" + settings.TPP_NOTIFICACION_URL + "",
                    "serviceDate": str(spain_time.year) + '-' + str(spain_time.month) + '-' + str(spain_time.day),
                    "client": client,
                    "directPayment": "true",
                    "paymentMethods": ["EXT", "TPP"]
                }

                payload_tpp = json.dumps(payload_tpp)
                headers = {
                    'Content-Type': "application/json",
                    'Authorization': "Bearer " + token
                }
                conn.request("POST", "/api/v2/paymentcards", payload_tpp, headers)
                res = conn.getresponse()
                data = res.read()
                retorno = data.decode("utf-8")
                if 'error' in json.loads(retorno):
                    return JsonResponse({'status': 400})
                else:
                    retorno = json.loads(retorno)['shortUrl']
                    orden.link_de_pago = retorno
                    orden.total = float('{:.2f}'.format(orden_total)) / 100
                    orden.save()
                    return JsonResponse({'status': 200, 'payment_link': orden.link_de_pago})
        else:
            return JsonResponse({'status': 400})


@method_decorator(csrf_exempt)
def tpp_success(request):
    uuid: str = request.GET.get('reference')
    uuid = uuid.replace('-', '')
    if Orden.objects.filter(pk=uuid).exists():
        orden = Orden.objects.get(pk=uuid)
        import time
        t_end = time.time() + 5
        while time.time() < t_end:
            if orden.status == '1':
                mensaje = create_message_order(request, orden)
                return redirect(
                    f'https://api.whatsapp.com/send/?phone=+{GeneralData.objects.all().first().phone_number}&text='
                    + mensaje.replace(" <br/> ", "\n") + '&app_absent=1')
        # Mandar pal fail
        return render(request, 'order_fail.html', {'uuid': uuid, 'business': GeneralData.objects.first()})
    return render(request, 'order_fail.html', {'uuid': uuid, 'business': GeneralData.objects.first()})


# TPP_Notification
@method_decorator(csrf_exempt)
def tpp_verificar(request: HttpRequest):
    if request.method == 'POST':
        payload = json.loads(request.body)
        bankOrderCode = payload['data']['bankOrderCode']
        originalCurrencyAmount = payload['data']['originalCurrencyAmount']
        signature = payload['data']['signature']
        status = payload['status']
        referencia = payload['data']['reference']
        cadena = bankOrderCode + settings.TPP_CLIENT_EMAIL + sha1(
            settings.TPP_CLIENT_PASSWORD.encode('utf-8')).hexdigest() \
                 + originalCurrencyAmount
        cadena = cadena.encode('utf-8')
        firma = sha256(cadena).hexdigest()
        if firma == signature:
            orden = get_object_or_404(Orden, pk=referencia)
            if status == 'OK':
                orden.status = '1'
                # Hice el descuento
                for i in orden.componente_orden.all():
                    prod = i.producto
                    prod.stock -= i.cantidad
                    prod.sales += i.cantidad
                    prod.save()
            else:
                orden.status = '2'
            orden.link_de_pago = "CONSUMIDO"
            orden.save()
            return HttpResponse('Verificando...')
    # fails alerta
    return render(request, 'order_fail.html',
                  {'uuid': request.session['last_order'], 'business': GeneralData.objects.first()})


@csrf_exempt
def pagar_cup(request: HttpRequest):
    if request.method == 'POST':
        if GeneralData.objects.all()[0].checkout_allowed == True:
            purchase_data = json.loads(request.body.decode('utf-8'))
            purchase_data['cart_id'] = request.headers.get('X-Session-ID')
            orden = create_order(purchase_data, 'CUP', **{})
            if orden:
                mensaje = create_message_order(request, orden)
                return JsonResponse({'status': 200,
                                     'payment_link': f'https://api.whatsapp.com/send/?phone={GeneralData.objects.all().first().phone_number}&text=[TEXTPLACEHOLDER]&app_absent=1',
                                     'wa_message':mensaje})
        else:
            return JsonResponse({'status': 400})
    return JsonResponse({'status': 400, 'return_url': 'https://gaia-mercado.com'})


def create_order(purchase_data, moneda, **kwargs):
    # Datos del formulario
    comprador = purchase_data['comprador']
    phone_comprador = purchase_data['phone_comprador']
    correo = purchase_data['email_comprador'] if moneda == 'Euro' else None
    municipio = Municipio.objects.get(pk=purchase_data['municipio'])
    nombre_municipio = municipio.nombre
    calle = purchase_data['calle']
    entre1 = purchase_data['entre1']
    entre2 = purchase_data['entre2']
    numero = purchase_data['numero']
    detalle = purchase_data['detalle']
    precio_envio = municipio.precio if moneda == 'CUP' else municipio.precio_euro
    # Calcular total
    cart = Cart()
    cart.session = purchase_data['cart_id']
    total = 0
    taza_cambio = 1 if moneda == 'CUP' else GeneralData.objects.all().first().taza_cambio
    tiempo_de_entrega = 0
    if cart.all():
        products = Product.objects.filter(pk__in=cart.all())
        for c in products:
            total += float(c.price) / taza_cambio * int(cache.get(cart.session)[str(c.id)])
            if int(c.delivery_time) > tiempo_de_entrega:
                tiempo_de_entrega = int(c.delivery_time)
        total += municipio.precio if moneda == 'CUP' else municipio.precio_euro
        orden = Orden(total=float(total), precio_envio=float(precio_envio), moneda=moneda,
                      status='1' if moneda == 'CUP' else '2', nombre_comprador=comprador,
                      telefono_comprador=phone_comprador, municipio=nombre_municipio, calle=calle,
                      calle1=entre1, calle2=entre2, numero_edificio=numero,
                      detalles_direccion=detalle, tiempo_de_entrega=tiempo_de_entrega)
        if correo:
            orden.correo = correo
        orden.save()
        for c in products:
            ComponenteOrden.objects.create(orden=orden, producto=c,
                                           respaldo=float(
                                               float(c.price) / taza_cambio * int(cache.get(cart.session)[str(c.id)])),
                                           cantidad=int(cache.get(cart.session)[str(c.id)]))
            # Aki se rebaja
            if moneda == 'CUP':
                c.stock = c.stock - int(cache.get(cart.session)[str(c.id)])
                c.sales += int(cache.get(cart.session)[str(c.id)])
                c.save()
        # Limpiar cart
        cart = cache.get(purchase_data['cart_id'])
        for product_id in list(cart.keys()):
            del cart[str(product_id)]
        cache.set(purchase_data['cart_id'], None)
        return orden
    return None


def create_message_order(request, orden):
    mensaje = 'Orden de compra:\n'
    mensaje += 'Ticket: ' + f'{str(orden.uuid)}\n'
    mensaje += 'Comprador: ' + orden.nombre_comprador + '\n'
    mensaje += 'Teléfono del comprador: ' + orden.telefono_comprador + '\n'
    mensaje += 'Precio de envío: ' + str(orden.precio_envio) + f' {orden.moneda}\n'
    mensaje += 'Precio total: ' + '{:.2f}'.format(orden.total) + f' {orden.moneda}\n'
    mensaje += 'Tiempo máximo de entrega: ' + str(orden.tiempo_de_entrega) + ' días\n\n'
    mensaje += 'Productos comprados: \n'
    for c in orden.componente_orden.all():
        mensaje += str(c) + '\n'
    mensaje += '\nDatos de entrega:\n'
    mensaje += f'Reparto: {orden.municipio}.\n'
    mensaje += f'Calle: {orden.calle}, entre {orden.calle1} y {orden.calle2}, No {orden.numero_edificio}.\n'
    mensaje += f' {orden.detalles_direccion}'
    return mensaje


def cancel_order(request, *args, **kwargs):
    orden = Orden.objects.get(pk=kwargs.get('pk'))
    orden.status = '3'
    orden.save()
    for c in orden.componente_orden.all():
        if c.producto:
            prod = c.producto
            prod.stock = prod.stock + c.cantidad
            prod.sales -= c.cantidad
            prod.save()
    return redirect('index-cup')


def fail_order(request):
    if 'last_order' in request.session:
        return render(request, template_name='order_fail.html',
                      context={'uuid': request.session['last_order'], 'business': GeneralData.objects.first()})
    return redirect('index-euro')


class OrdenAPIList(generics.ListCreateAPIView):
    serializer_class = OrdenSerializer
    queryset = Orden.objects.all()


class OrdenAPIDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrdenSerializer
    queryset = Orden.objects.all()
    lookup_field = 'uuid'


def change_active_session_ajax(request):
    del request.session['active']
    request.session['active'] = str(request.POST['active_session'])
    return JsonResponse({"result": "ok", "active": request.session['active']})


def whole_products(request):
    products = ""
    for product in Product.objects.all():
        products = products + '{} - {}'.format(product.name, str(product.price))
    return JsonResponse({"result": products, "active": "1"})
