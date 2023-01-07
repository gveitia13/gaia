from django.urls import path

from app_main.views import StartPage, create_suscriptor, ProductView

urlpatterns = [
    path('', StartPage.as_view(), name='index'),
    path('suscriptor_create/', create_suscriptor, name='suscriptor'),
    path('products/', ProductView.as_view(), name='products'),
]
