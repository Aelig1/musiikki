from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core import serializers
import json

from metadata.models import Artist, Album, Track

def ui(request):
	return render(request, 'ui.html')

def artist(request, id):
	# Find artist
	try:
		artist = Artist.objects.get(id=id)
	except Artist.DoesNotExist:
		raise Http404('Artist with ID ' + id + ' does not exist.')
	
	# Examine request
	if request.method == 'GET':
		# Check callback
		callback = request.GET.get('callback')
		if (callback != None):
			# Stringify aritst inside callback function call
			json_data = callback + '(' + json.dumps(artist.dict()) + ');'
		else:
			# No callback, stringify with indentation
			json_data = json.dumps(artist.dict(), indent=2)
		
		return HttpResponse(json_data, content_type='application/json')
	
	elif request.method == 'POST':
		# Conflict, artist already exists
		return HttpResponse(status=409)
		
	elif request.method == 'PUT':
		# TODO
		return HttpResponse()
	
	elif request.method == 'PATCH':
		# TODO
		return HttpResponse()
	
	elif request.method == 'DELETE':
		# Delete artist
		artist.delete()
		return HttpResponse()
	
	return HttpResponse(status=405)

def artists(request):
	# Examine request
	if request.method == 'GET':
		artists = []
		for artist in Artist.objects.all():
			artists.append(artist.dict())
		
		# Check callback
		callback = request.GET.get('callback')
		if (callback != None):
			# Stringify aritsts inside callback function call
			json_data = callback + '(' + json.dumps(artists) + ');'
		else:
			# No callback, stringify with indentation
			json_data = json.dumps(artists, indent=2)
			
		return HttpResponse(json_data, content_type='application/json')
	
	elif request.method == 'POST':
		print(request.POST.get('artist_id'))
		return HttpResponse(status=201)
	
	return HttpResponse(status=405)

def album(request, id):
	# Find album
	try:
		album = Album.objects.get(id=id)
	except Album.DoesNotExist:
		raise Http404('Album with ID ' + id + ' does not exist.')
	
	# Examine request
	if request.method == 'GET':
		# Check callback
		callback = request.GET.get('callback')
		if (callback != None):
			# Stringify album inside callback function call
			json_data = callback + '(' + json.dumps(album.dict()) + ');'
		else:
			# No callback, stringify with indentation
			json_data = json.dumps(album.dict(), indent=2)
		
		return HttpResponse(json_data, content_type='application/json')
	
	elif request.method == 'PUT':
		pass
	
	elif request.method == 'DELETE':
		pass
	
	return HttpResponse(id, content_type='application/json')

def track(request, id):
	# Find track
	try:
		track = Track.objects.get(id=id)
	except Track.DoesNotExist:
		raise Http404('Track with ID ' + id + ' does not exist.')
	
	# Examine request
	if request.method == 'GET':
		# Check callback
		callback = request.GET.get('callback')
		if (callback != None):
			# Stringify track inside callback function call
			json_data = callback + '(' + json.dumps(track.dict()) + ');'
		else:
			# No callback, stringify with indentation
			json_data = json.dumps(track.dict(), indent=2)
		
		return HttpResponse(json_data, content_type='application/json')
	
	elif request.method == 'PUT':
		pass
	
	elif request.method == 'DELETE':
		pass
	
	return HttpResponse(id, content_type='application/json')
	
def search(request):
	return JSONResponse(request.GET.dict())

def JSONResponse(dict):
	'''
	try:
		artist_id = dict['artist_id']
	    try:
	        artist = Artist.objects.get(code=artist_id)
	    except Artist.DoesNotExist:
	        raise Http404('Continent \"' + art + '\" does not exist')
	except KeyError:
		pass
	'''
	return HttpResponse("JSON", content_type='application/json')
