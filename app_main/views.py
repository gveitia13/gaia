import datetime
import http.client
import json
from hashlib import sha256, sha1

import pytz
from django.forms import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.decorators.http import require_POST
from rest_framework import generics, status
from rest_framework.response import Response

from app_cart.cart import Cart
from app_main.models import Product, Category, GeneralData, Banner, Suscriptor, InfoUtil, Municipio, Orden, \
    ComponenteOrden
from app_main.serializers import OrdenSerializer
from gaia import settings


class BaseView(View):

    def get_my_context_data(self, **kwargs):
        cart = Cart(self.request)
        # print('products_in_cart', json.dumps(cart.all(), indent=3))
        # print('products_in_cart', cart.all())
        c_x_p = len(cart.all())
        # print(c_x_p)
        print('host', self.request.get_host())
        if self.request.get_host().__contains__("127.0.0.1") or self.request.get_host().__contains__(
                "localhost") or self.request.get_host().__contains__("192.168"):
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
            'host': host + self.request.get_host() + '/',
            'address': Municipio.objects.all()
        }


class StartPage(BaseView, generic.ListView, ):
    template_name = 'startpage.html'
    queryset = Product.objects.filter(is_active=True, stock__gt=0)
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
        # print(qs)
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
        context['categories'] = sorted(Category.objects.filter(product__isnull=False, destacado=True).distinct(),
                                       key=lambda cat: cat.get_prods_count, reverse=True)[0:4]
        context['products_destacados'] = Product.objects.filter(is_active=True, is_important=True)[0:10]
        context['products_descuento'] = Product.objects.filter(is_active=True, old_price__isnull=False)[0:10]
        context['products_nuevos'] = Product.objects.filter(is_active=True).order_by('-pk')[0:10]

        context['carousel'] = [b.banner.url for b in Banner.objects.filter(gnd=gnd)] if gnd else [
            settings.STATIC_URL / settings.BUSINESS_BANNER]
        # context['index_url'] = self.request.session['index_url']
        print(self.request.META.get('HTTP_REFERER'))
        print(self.request.path)
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
    queryset = Product.objects.filter(is_active=True, stock__gt=0).exclude(moneda='Euro')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['moneda'] = 'CUP'
        context['categories'] = sorted(
            Category.objects.filter(product__isnull=False, destacado=True,
                                    product__moneda__in=['CUP', 'Ambas']).distinct(),
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
    queryset = Product.objects.filter(is_active=True, stock__gt=0).exclude(moneda='CUP')
    template_name = 'startpage_euro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['moneda'] = 'Euro'
        context['categories'] = sorted(
            Category.objects.filter(product__isnull=False, destacado=True,
                                    product__moneda__in=['Euro', 'Ambas']).distinct(),
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
        context['categories'] = sorted(Category.objects.filter(product__isnull=False, destacado=True).distinct(),
                                       key=lambda cat: cat.get_prods_count, reverse=True)[0:4]
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
        context['is_euro'] = True
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


def pagar_euro(request):
    if request.method == 'POST':
        orden = create_order(request, 'Euro', **{})
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
            token = token.split(':')[1].split(',')[0].replace('"', '').replace(' ', '')

            user_comprador = orden.nombre_comprador

            # Convertir total a 2 decimales
            address = 'Municipio: ' + orden.municipio + '. '
            address += 'Calle: ' + orden.calle + '. '
            address += 'Entre calle : ' + orden.calle1 + ' y calle ' + orden.calle2 + '. '
            address += 'Número: ' + orden.numero_edificio + '. '
            address += 'Reparto: ' + orden.reparto + '. '
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

            spain_timezone = pytz.timezone("Europe/Madrid")
            spain_time = datetime.datetime.now(spain_timezone)
            payload_tpp = {
                "reference": str(orden.uuid),
                "concept": "Orden de GAIA a nombre de " + client['email'],
                "favorite": "false",
                "description": mensaje,
                "amount": float('{:.2f}'.format(orden.total)) * 100,  # para quitar decimales
                "currency": 'EUR',
                "singleUse": "true",
                "reasonId": 4,
                "expirationDays": 10,
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
            print('retorno aki', retorno)
            retorno = retorno.split(',')
            retorno = retorno[len(retorno) - 2].replace('"shortUrl":"', '').replace('"', '')
            orden.link_de_pago = retorno
            orden.total = float('{:.2f}'.format(orden.total)) / 100

            orden.save()
            print('orden d pago va aki', orden.link_de_pago)
            return redirect(orden.link_de_pago)


def tpp_verificar(request):
    if request.method == 'POST':
        payload = json.loads(str(request.data).replace('\'', '"'))
        bankOrderCode = ""
        originalCurrencyAmount = ""
        signature = ""
        status = payload['status']
        referencia = ""
        for key, value in payload.items():
            if key == 'data':
                datos = json.loads(str(payload['data']).replace('\'', '"'))
                bankOrderCode = datos['bankOrderCode']
                originalCurrencyAmount = datos['originalCurrencyAmount']
                signature = datos['signature']
                referencia = datos['reference']
        cadena = bankOrderCode + settings.TPP_CLIENT_EMAIL + sha1(
            settings.TPP_CLIENT_PASSWORD.encode('utf-8')).hexdigest() \
                 + originalCurrencyAmount
        cadena = cadena.encode('utf-8')
        firma = sha256(cadena).hexdigest()
        if firma == signature:
            orden = get_object_or_404(Orden, pk=referencia)
            if status == 'OK':
                orden.status = '1'
            else:
                orden.status = '2'
            orden.link_de_pago = "CONSUMIDO"
            orden.save()

            mensaje = create_message_order(request, orden)
            return redirect(
                f'https://api.whatsapp.com/send/?phone=+{GeneralData.objects.all().first().phone_number}&text=' +
                mensaje.replace(" <br/> ", "\n") + '&app_absent=1')
        return redirect('index-euro')
    return redirect('index-euro')


def pagar_cup(request: HttpRequest):
    if request.method == 'POST':
        orden = create_order(request, 'CUP', **{})
        if orden:
            mensaje = create_message_order(request, orden)
            return redirect(
                f'https://api.whatsapp.com/send/?phone=+{GeneralData.objects.all().first().phone_number}&text=' + mensaje.replace(
                    " <br/> ", "\n") + '&app_absent=1')
    return redirect('index-cup')


def create_order(request: HttpRequest, moneda, **kwargs):
    # Datos del formulario
    comprador = request.POST.get('comprador')
    phone_comprador = request.POST.get('phone_comprador')
    correo = request.POST.get('email_comprador')
    receptor = request.POST.get('receptor')
    phone_receptor = request.POST.get('phone_receptor')
    municipio = Municipio.objects.get(pk=request.POST.get('municipio'))
    nombre_municipio = municipio.nombre
    calle = request.POST.get('calle')
    entre1 = request.POST.get('entre1')
    entre2 = request.POST.get('entre2')
    numero = request.POST.get('numero')
    reparto = request.POST.get('reparto')
    detalle = request.POST.get('detalle')
    precio_envio = municipio.precio if moneda == 'CUP' else municipio.precio_euro
    # Calcular total
    cart = Cart(request)
    total = 0
    taza_cambio = 1 if moneda == 'CUP' else GeneralData.objects.all().first().taza_cambio
    tiempo_de_entrega = 0
    if cart.all():
        for c in cart.all():
            total += c['product']['price'] / taza_cambio * c['quantity']
            if int(c['product']['delivery_time']) > tiempo_de_entrega:
                tiempo_de_entrega = int(c['product']['delivery_time'])
        total += municipio.precio if moneda == 'CUP' else municipio.precio_euro

        orden = Orden.objects.create(total=float(total), precio_envio=float(precio_envio), moneda=moneda,
                                     status='1' if moneda == 'CUP' else '2', nombre_comprador=comprador,
                                     telefono_comprador=phone_comprador, nombre_receptor=receptor,
                                     telefono_receptor=phone_receptor, municipio=nombre_municipio, calle=calle,
                                     calle1=entre1, calle2=entre2, numero_edificio=numero, reparto=reparto,
                                     detalles_direccion=detalle, tiempo_de_entrega=tiempo_de_entrega, correo=correo)
        for c in cart.all():
            prod = Product.objects.get(pk=c['id'])
            ComponenteOrden.objects.create(orden=orden, producto=prod,
                                           respaldo=float(c['product']['price'] / taza_cambio * c['quantity']),
                                           cantidad=int(c['quantity']))
            prod.stock = prod.stock - int(c['quantity'])
            prod.sales += int(c['quantity'])
            prod.save()
        # Limpiar cart
        Cart(request).clear()
        return orden
    return None


def create_message_order(request, orden):
    mensaje = 'Orden de compra:\n'
    print(orden)
    mensaje += 'Comprador: ' + orden.nombre_comprador + '\n'
    mensaje += 'Teléfono del comprador: ' + orden.telefono_comprador + '\n'
    mensaje += 'Receptor: ' + orden.nombre_receptor + '\n'
    mensaje += 'Teléfono del receptor: ' + orden.telefono_receptor + '\n'
    mensaje += 'Precio de envío: ' + str(orden.precio_envio) + f' {orden.moneda}\n'
    mensaje += 'Precio total: ' + '{:.2f}'.format(orden.total) + f' {orden.moneda}\n'
    mensaje += 'Tiempo máximo de entrega: ' + str(orden.tiempo_de_entrega) + ' días\n\n'
    mensaje += 'Productos comprados: \n'
    for c in orden.componente_orden.all():
        mensaje += str(c) + '\n'
    mensaje += '\nPara cancelar su orden abra el siguiente enlace: \n'
    host = 'http://' if request.get_host().__contains__("127.0.0.1") or request.get_host().__contains__(
        "localhost") or request.get_host().__contains__("192.168") else 'https://'

    mensaje += f'{host}' + request.get_host() + reverse_lazy('cancelar', kwargs={'pk': orden.pk})
    print(mensaje)
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


class OrdenAPIList(generics.ListCreateAPIView):
    serializer_class = OrdenSerializer
    queryset = Orden.objects.all()

    def list(self, request, *args, **kwargs):
        data = [i.toJSON() for i in self.get_queryset()]
        return Response(data=data, status=status.HTTP_200_OK)


class OrdenAPIDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrdenSerializer
    queryset = Orden.objects.all()
    lookup_field = 'uuid'
