from django.conf.urls import url, include
from rest_framework import routers
from yt import views

from yt.views import index

from . import views

#urlpatterns = [
 #   url(r'^$', index.as_view(), name='index'),
#]

#urlpatterns = [
 #   path('', views.index, name='index'),
#]

router = routers.DefaultRouter()

router.register(r'YoutubeStat', views.YoutubeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'^$', index.as_view(), name='index'),
    url(r'^api/', include(router.urls)),

]