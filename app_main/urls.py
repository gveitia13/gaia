from django.shortcuts import redirect
from django.urls import path

from app_main.views import *


def asd(request):
    return redirect('index-cup')


urlpatterns = [
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
