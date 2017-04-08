# musiikki URL Configuration
from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.contrib import admin

from rest import urls as rest_urls

urlpatterns = [
	url(r'^$', RedirectView.as_view(url='api')),
	url(r'^admin/', admin.site.urls),
	url(r'^api/', include(rest_urls))
]
