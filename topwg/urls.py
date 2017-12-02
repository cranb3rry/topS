from django.conf.urls import url

from topwg.views import MyView, TopWgHome

urlpatterns = [
    url(r'^$', TopWgHome.as_view(), name='index'),
]