"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^msg/', include('vcmesg.urls')),
    url(r'^nt/', include('notifier.urls')),
    url(r'^ue4/', include('ue4.urls')),
    url(r'^ue4/', include('ue4.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^yt/', include('yt.urls')),
    url(r'^sn/', include('sn.urls')),
    url(r'^topfeed/', include('topfeed.urls')),
    url(r'^topwa/', include('topwa.urls')),
    url(r'^topwg/', include('topwg.urls')),
    url(r'^toptv/', include('toptv.urls')),
    url(r'^tw/', include('tw.urls')),
    url(r'^topr/', include('topr.urls')),
	url(r'^', include('home.urls')),
	url(r'^', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)