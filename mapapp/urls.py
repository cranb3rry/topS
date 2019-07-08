from django.conf.urls import url, include
from django.urls import path

from mapapp.views import index, widget

urlpatterns = [
    path('', index.as_view(), name='index'),
	path('widget/', widget.as_view(), name='widget'),

]