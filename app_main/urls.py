from django.urls import path

from app_main.views import StartPage, create_suscriptor, ProductView, InfoView, CatalogoView, delete_suscriptor

# def correo(request):
#     return render(request=request, template_name='correo/index.html',
#                   context={'prod': Product.objects.first(), 'cfg': GeneralData.objects.first(),
#                            'info': InfoUtil.objects.all()[:3], 'email': 'gveitia95@gmail.com'})


urlpatterns = [
    path('', StartPage.as_view(), name='index'),
    path('suscriptor_create/', create_suscriptor, name='suscriptor'),
    path('products/', ProductView.as_view(), name='products'),
    path('info/', InfoView.as_view(), name='info'),
    path('catalogo/', CatalogoView.as_view(), name='catalogo'),
    # path('correo/', correo, name='correo'),
    path('suscriptor_delete/<email>/', delete_suscriptor, name='del-suscriptor')
]
