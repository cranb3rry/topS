from django.conf.urls import url

from topwg.views import MyView

urlpatterns = [
    url(r'^$', MyView.as_view(), name='my-view'),
]