from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

#class index(TemplateView):

    #template_name = "../static/index.html"

def index(request):
    return render('static/ue4/index.html')