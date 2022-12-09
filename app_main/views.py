from django.shortcuts import render
from django.views import generic


class StartPage(generic.TemplateView):
    template_name = 'index.html'
