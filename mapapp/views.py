from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.

class index(TemplateView):

    template_name = "mapapp/map_view.html"

class widget(TemplateView):

    template_name = "mapapp/widget.html"