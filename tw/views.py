import requests
import time

from django.views.generic.base import TemplateView

from django.http import HttpResponse

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from tw.serializers import UserSerializer, GroupSerializer, TwitchSerializer
from tw.models import TwitchStat



# Create your views here.

class index(TemplateView):
    model = TwitchStat
    template_name = "tw/index.html"
    def get_queryset(self):
        s = TwitchStat.objects.get(name='mainstats')
        views, subs, status = s.views, s.subs, s.status
        return views, subs, status

#def index(request):
 #   return HttpResponse("Hello, world. You're at the polls index.")

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class TwitchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = TwitchStat.objects.all()
    serializer_class = TwitchSerializer

