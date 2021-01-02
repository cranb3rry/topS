from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('dnt/', views.dnt, name='dnt'),
    path('pdl/', views.pdl, name='pdl'),
    path('pxs/', views.pxs, name='pxs'),
]