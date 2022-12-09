from django.urls import path

from app_main.views import StartPage

urlpatterns = [
    path('', StartPage.as_view(), name='index'),
]
