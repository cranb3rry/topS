from django.conf.urls import url, include

from notifier import views

from notifier.views import HomeView


#urlpatterns = [
 #   url(r'^$', index.as_view(), name='index'),
#]

#urlpatterns = [
 #   path('', views.index, name='index'),
#]

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
	url(r'', HomeView.as_view(), name='HomeView'),
]