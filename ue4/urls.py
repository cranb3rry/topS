from django.conf.urls import url, include
from ue4.views import index

urlpatterns = [
    url(r'^$', index),
]