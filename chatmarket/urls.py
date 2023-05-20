from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import path

from chatmarket.views import *




urlpatterns = [
    path('', index, name='index'),
    path('*', lambda request: HttpResponseNotFound('404 Not Found'))
]
