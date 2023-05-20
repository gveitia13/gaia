from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import path

from chatmarket.views import *




urlpatterns = [
    path('', meta_wa_callbackurl, name='meta_wa_callbackurl'),
    path('*', lambda request: HttpResponseNotFound('404 Not Found'))
]
