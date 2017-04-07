from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^add$', views.add),
	url(r'^modify$', views.modify),
	url(r'^remove$', views.remove),
    url(r'^search$', views.search)
]
