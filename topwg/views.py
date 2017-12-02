from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views import View


class MyView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')

class HomePageView(TemplateView):

    template_name = "home.html"