from django.http import HttpResponse, Http404
import json

from metadata.models import Artist, Album, Track

def add(request):
	return HttpResponse("add", content_type='application/json')

def modify(request):
	return HttpResponse("modify", content_type='application/json')

def remove(request):
	return HttpResponse("remove", content_type='application/json')

def search(request):
	return HttpResponse("search JSON", content_type='application/json')
