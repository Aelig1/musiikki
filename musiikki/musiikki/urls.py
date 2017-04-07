# musiikki URL Configuration

from django.conf.urls import include, url
from django.contrib import admin

from rest import urls as rest_urls

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^api/', include(rest_urls))
]
