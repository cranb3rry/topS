import requests
import time

from django.views.generic.base import TemplateView

from django.http import HttpResponse

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from yt.serializers import YoutubeSerializer
from yt.models import YoutubeStat



# Create your views here.

class index(TemplateView):
    model = YoutubeStat
    template_name = "yt/index.html"
    def get_queryset(self):
        s = YoutubeStat.objects.get(name='mainstats')
        views, subs, status = s.views, s.subs, s.status
        return views, subs, status

#def index(request):
 #   return HttpResponse("Hello, world. You're at the polls index.")


class YoutubeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = YoutubeStat.objects.all()
    serializer_class = YoutubeSerializer

