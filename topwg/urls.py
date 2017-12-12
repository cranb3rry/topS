from django.conf.urls import url

from topwg.views import TopWgHome

urlpatterns = [
    url(r'^$', TopWgHome.as_view(), name='index'),
]