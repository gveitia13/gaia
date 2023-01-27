from django.shortcuts import redirect
from django.urls import path

from app_main.views import create_suscriptor, InfoView, delete_suscriptor, \
    StartPageCUP, StartPageEuro, CatalogoEuroView, CatalogoCUPView, pagar_euro, tpp_verificar, pagar_cup, \
    cancel_order


# def correo(request):
#     return render(request=request, template_name='correo/index.html',
#                   context={'prod': Product.objects.first(), 'cfg': GeneralData.objects.first(),
#                            'info': InfoUtil.objects.all()[:3], 'email': 'gveitia95@gmail.com'})

def asd(request):
    return redirect('index-cup')


urlpatterns = [
    path('', asd, name='asd'),
    path('CUP/', StartPageCUP.as_view(), name='index-cup'),  # CUP
    path('Euro/', StartPageEuro.as_view(), name='index-euro'),  # CUP
    path('suscriptor_create/', create_suscriptor, name='suscriptor'),
    path('info/', InfoView.as_view(), name='info'),
    path('catalogo/CUP/', CatalogoCUPView.as_view(), name='catalogo-cup'),
    path('catalogo/Euro/', CatalogoEuroView.as_view(), name='catalogo-euro'),
    path('suscriptor_delete/<email>/', delete_suscriptor, name='del-suscriptor'),
    # EURO
    path('pagar/euro/', pagar_euro, name='pagar-euro'),
    path('tropipay/verificar/', tpp_verificar, name='tpp_verificar'),
    # CUP
    path('pagar/cup/', pagar_cup, name='pagar-cup'),
    path('cancelar_orden/<pk>/', cancel_order, name='cancelar'),
]
