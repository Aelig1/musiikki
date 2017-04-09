from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.ui),
	url(r'^artist/(\d+)$', views.artist),
	url(r'^artists$', views.artists),
	url(r'^album/(\d+)$', views.album),
	url(r'^track/(\d+)$', views.track),
	url(r'^search$', views.search)
]
