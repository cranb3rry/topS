from django.conf.urls import url, include
from rest_framework import routers
from tw import views

from tw.views import index

from . import views

#urlpatterns = [
 #   url(r'^$', index.as_view(), name='index'),
#]

#urlpatterns = [
 #   path('', views.index, name='index'),
#]

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
router.register(r'twitchstat', views.TwitchViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'^$', index.as_view(), name='index'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]