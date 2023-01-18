from django.shortcuts import redirect
from django.urls import path

from app_main.views import StartPage, create_suscriptor, ProductView, InfoView, CatalogoView, delete_suscriptor, \
    StartPageCUP, StartPageEuro


# def correo(request):
#     return render(request=request, template_name='correo/index.html',
#                   context={'prod': Product.objects.first(), 'cfg': GeneralData.objects.first(),
#                            'info': InfoUtil.objects.all()[:3], 'email': 'gveitia95@gmail.com'})

def asd(request):
    return redirect('index-cup')


urlpatterns = [
    path('', asd, name='asd'),
    # path('index/', StartPage.as_view(), name='index'),  # todos
    # path('index/<moneda>/', StartPage.as_view(), name='index-filter'),  # CUP
    path('CUP/', StartPageCUP.as_view(), name='index-cup'),  # CUP
    path('Euro/', StartPageEuro.as_view(), name='index-euro'),  # CUP
    path('suscriptor_create/', create_suscriptor, name='suscriptor'),
    path('products/', ProductView.as_view(), name='products'),
    path('info/', InfoView.as_view(), name='info'),
    path('catalogo/', CatalogoView.as_view(), name='catalogo'),
    # path('correo/', correo, name='correo'),
    path('suscriptor_delete/<email>/', delete_suscriptor, name='del-suscriptor')
]
