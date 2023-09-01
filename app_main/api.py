import random

from django.db.models import Q, Count
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app_cart.cart import Cart
from gaia import settings
from .models import GeneralData, InfoUtil, Category, Municipio, Product
from .views import BaseView, StartPage
from .serializers import ProductSerializer, GeneralDataSerializer, InfoUtilSerializer, CategorySerializer, \
    MunicipioSerializer


def get_context_data(currency=None):
    business = GeneralData.objects.all()[0]
    if business:
        business_data = GeneralDataSerializer(business).data
    else:
        business_data = {}
    if len(InfoUtil.objects.filter(contenidoinfo__isnull=False).distinct()):
        infoUtil_list = InfoUtil.objects.filter(contenidoinfo__isnull=False).distinct()[:4]
    else:
        infoUtil_list = InfoUtil.objects.filter(contenidoinfo__isnull=False).distinct()
    infoUtil_data = InfoUtilSerializer(infoUtil_list, many=True, context = {'esential' : True}).data
    if currency == 'CUP':
        all_categories = sorted(
            Category.objects.filter(product__isnull=False, destacado=True, product__is_active=True,
                                    product__moneda__in=['CUP', 'Ambas']).distinct(),
            key=lambda cat: cat.get_prods_count, reverse=True)
    else:
        all_categories = sorted(
            Category.objects.filter(product__isnull=False, destacado=True, product__is_active=True,
                                    product__moneda__in=['Euro', 'Ambas']).distinct(),
            key=lambda cat: cat.get_prods_count, reverse=True)
    if len(all_categories) > 4:
        all_categories = random.sample(all_categories, 4)
    else:
        all_categories = random.sample(all_categories, len(all_categories))
    all_categories_data = CategorySerializer(all_categories, many=True).data
    address = Municipio.objects.filter(visible=True)
    address_data = MunicipioSerializer(address, many=True).data
    return {
        'business': business_data,
        'infoUtil_list': infoUtil_data,
        'all_categories': all_categories_data,
        'address': address_data,
    }

class BaseViewSet(viewsets.ViewSet):
    def list(self, request):
        # cart = Cart(self.request)
        # c_x_p = len(cart.all())

        if self.request.get_host().__contains__("127.0.0.1") or self.request.get_host().__contains__(
                "localhost"):
            host = 'http://'
        else:
            host = 'https://'
        context_data_result = get_context_data(currency=request.headers.get('currency'))
        context_data =  {
            'icon': settings.BUSINESS_LOGO_PATH,
            'title': settings.BUSINESS_NAME,
            'logo': settings.BUSINESS_NAME_IMG_PATH,
            'banner': settings.BUSINESS_BANNER,
            'business': context_data_result['business'],
            'products_in_cart': {},
            'total_price': '',
            'infoUtil_list': context_data_result['infoUtil_list'],
            'all_categories': context_data_result['all_categories'],
            'host': host + self.request.get_host() + '/' if settings.TECHNOSTAR else 'https://gaia-mercado.com/',
            'address': context_data_result['address'],
        }
        return Response(context_data)

class StartPageViewSet(viewsets.ViewSet):

    def list(self, request):
        view = StartPage(request=request)
        context_data = view.get_context_data()
        print(context_data)
        return Response(context_data)

class ImportantProductsView(APIView):
    def get(self, request):
        products = Product.objects.filter(
            Q(moneda=request.headers['currency']) | Q(moneda='Ambas'),
            is_active=True,
            is_important=True
        )[0:10]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class OnSaleProductsView(APIView):
    def get(self, request):
        products = Product.objects.filter(
            Q(moneda=request.headers['currency']) | Q(moneda='Ambas'),
            is_active=True,
            old_price__isnull=False
        )[0:10]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class QuickInitialView(APIView):
    def get(self, request):
        business = GeneralData.objects.all()[0]
        return Response({'exchange': business.taza_cambio})

class NewProductsView(APIView):
    def get(self, request):
        products = Product.objects.filter(
            Q(moneda=request.headers['currency']) | Q(moneda='Ambas'),
            is_active=True,
        ).order_by('-pk')[0:10]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(prods_count=Count('product')).filter(prods_count__gt=0)
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

class InfoUtilList(ListAPIView):
    serializer_class = InfoUtilSerializer

    def get_queryset(self):
        # Filter the queryset to only include InfoUtil instances with at least one related ContenidoInfo object
        queryset = InfoUtil.objects.filter(contenidoinfo__isnull=False).distinct()
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['esential'] = self.request.query_params.get('esential', False)
        return context