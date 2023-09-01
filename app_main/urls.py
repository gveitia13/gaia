from django.shortcuts import redirect
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_main.api import BaseViewSet, StartPageViewSet, ImportantProductsView, OnSaleProductsView, NewProductsView, \
    CategoryViewSet, ProductViewSet, QuickInitialView, InfoUtilList
from app_main.views import *


router = DefaultRouter()
router.register(r'base', BaseViewSet, basename='base')
router.register(r'start_page', StartPageViewSet, basename='start_page')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')

def asd(request):
    return redirect('index-cup')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/quick/initial/', QuickInitialView.as_view(), name='quick_initial'),
    path('api/important_products/', ImportantProductsView.as_view(), name='important_products'),
    path('api/onsale_products/', OnSaleProductsView.as_view(), name='onsale_products'),
    path('api/new_products/', NewProductsView.as_view(), name='new_products'),
    path('api/infoutil/', InfoUtilList.as_view(), name='infoutil_list'),
    path('', asd, name='asd'),
    path('CUP/', StartPageCUP.as_view(), name='index-cup'),
    path('Euro/', StartPageEuro.as_view(), name='index-euro'),
    path('info/', InfoView.as_view(), name='info'),
    path('catalogo/CUP/', CatalogoCUPView.as_view(), name='catalogo-cup'),
    path('catalogo/Euro/', CatalogoEuroView.as_view(), name='catalogo-euro'),
    path('CUP/suscriptor_create/', create_suscriptor, name='suscriptor'),
    path('Euro/suscriptor_create/', create_suscriptor, name='suscriptor'),
    path('CUP/suscriptor_delete/<email>/', delete_suscriptor, name='del-suscriptor'),
    path('Euro/suscriptor_delete/<email>/', delete_suscriptor, name='del-suscriptor'),
    # EURO
    path('pagar/euro/', pagar_euro, name='pagar-euro'),
    path('tropipay/verificar/', tpp_verificar, name='tpp_verificar'),
    path('tropipay/success/', tpp_success, name='tpp_success'),
    path('tropipay/fails/', fail_order, name='orden-fail'),
    # CUP
    path('pagar/cup/', pagar_cup, name='pagar-cup'),
    path('cancelar_orden/<pk>/', cancel_order, name='cancelar'),
    # API
    path('orden/list/', OrdenAPIList.as_view(), name='orden-api-list'),
    path('orden/<uuid>/', OrdenAPIDetails.as_view(), name='orden-api-details'),
    #AJAX
    path('whole_products/', whole_products, name='whole_products'),
    path('session/change/', change_active_session_ajax, name='change_active_session_ajax'),
]
