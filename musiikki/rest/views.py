from django.shortcuts import render
from django.http import HttpResponse, Http404
import json

from metadata.models import Artist, Album, Track

def ui(request):
	return render(request, 'ui.html')

def modify(request):
	
	return HttpResponse("modify", content_type='application/json')

def search(request):
	# Artist
	artist_id = request.GET.get('artist_id')
	print(artist_id)
	artist = request.GET.get('artist')
	genre = request.GET.get('genre')
	# Album
	album_id = request.GET.get('album_id')
	album = request.GET.get('album')
	year = request.GET.get('year')	
	# Track
	track_id = request.GET.get('track_id')
	track = request.GET.get('track')
	
	return HttpResponse("search JSON", content_type='application/json')
