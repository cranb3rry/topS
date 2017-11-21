from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.hls, name='hls'),
    url(r'^hls/', views.hls, name='hls')
]