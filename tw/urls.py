from django.conf.urls import url

from tw.views import index

from . import views

urlpatterns = [
    url(r'^$', index.as_view(), name='index'),
]

#urlpatterns = [
 #   path('', views.index, name='index'),
#]