from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import datetime

def index(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return render(
        request,
        'home/index.html',
     
    )

def dnt(request):
    return render(request, 'home/dnt.html', {})

def pdl(request):
    return render(request, 'home/pdl.html', {})
