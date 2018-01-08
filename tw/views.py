
from django.views.generic.base import TemplateView

from django.http import HttpResponse
# Create your views here.

class index(TemplateView):

    template_name = "tw/index.html"

#def index(request):
 #   return HttpResponse("Hello, world. You're at the polls index.")