from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.ui),
	url(r'^modify$', views.modify),
	url(r'^search$', views.search)
]
