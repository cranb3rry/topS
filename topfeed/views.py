from .models import Feed
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import generic
# Create your views here.

class Index(TemplateView):

    template_name = "topfeed/index.html"