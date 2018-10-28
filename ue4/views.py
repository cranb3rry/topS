from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
# Create your views here.

#class index(TemplateView):

    #template_name = "../static/index.html"

def index(request):
    return render_to_response('static/ue4/index.html')