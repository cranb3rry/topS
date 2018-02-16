import requests
import time

from django.views.generic.base import TemplateView

from django.http import HttpResponse

from django.contrib.auth.models import User, Group




# Create your views here.

class index(TemplateView):

    template_name = "sn/index.html"


