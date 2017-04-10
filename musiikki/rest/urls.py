from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.ui),
	
	url(r'^artists/$', views.artists), # All artists
	url(r'^artists/(\d+)/$', views.artist), # Single artist
	url(r'^albums/$', views.albums), # All albums
	url(r'^albums/(\d+)/$', views.album), # Single album
	url(r'^tracks/$', views.tracks), # All tracks
	url(r'^tracks/(\d+)/$', views.track), # Single track
	
	url(r'^search/$', views.search)
]
