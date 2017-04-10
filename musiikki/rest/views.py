from django.shortcuts import render
from django.http import HttpResponse, Http404, QueryDict

from datetime import timedelta
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
	
	elif request.method == 'HEAD':
		return HttpResponse()
	
	elif request.method == 'POST':
		# Conflict, artist already exists
		return HttpResponse(status=409)
		
	elif request.method == 'PUT':
		put = QueryDict(request.body)
		# TODO: Replace ad hoc parameter extraction with automatic and dynamic
		# where not-null fields in model are required
		name = put.get('artist')
		if not name:
			return HttpResponse(status=400)
		
		genre = put.get('genre')
		if not genre:
			# Make null if empty string
			genre = None
		
		# Assign values
		artist.name = name
		artist.genre = genre
		artist.save()
		
		return HttpResponse()
	
	elif request.method == 'PATCH':
		patch = QueryDict(request.body)
		modified = False
		# TODO: Dynamic implementation
		name = patch.get('artist')
		if name:
			artist.name = name
			modified = True
		
		genre = patch.get('genre')
		if genre:
			artist.genre = genre
			modified = True
		
		if modified:
			artist.save()
		
		return HttpResponse()
	
	elif request.method == 'DELETE':
		# Delete artist
		artist.delete()
		return HttpResponse()
	
	return HttpResponse(status=405)

def artists(request):
	# Examine request
	if request.method == 'GET':
		# Get all artists
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
	
	elif request.method == 'HEAD':
		return HttpResponse()
	
	elif request.method == 'POST':
		# Create new artist
		artist = request.POST.get('artist')
		genre = request.POST.get('genre')
		
		if not artist:
			# Artist name required
			return HttpResponse(status=400)
		if not genre:
			# Reformat empty genre
			genre = None
		
		artist = Artist.objects.create(name=artist, genre=genre)
		if not artist:
			# Artist was not created
			return HttpResponse(status=507)
		
		response = HttpResponse(status=201)
		response['location'] = artist.id
		return response
	
	elif request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
		return HttpResponse(status=404)
	
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
	
	return HttpResponse(id, content_type='application/json')

def albums(request):
	# Examine request
	if request.method == 'GET':
		# Get all albums
		albums = []
		for album in Album.objects.all():
			albums.append(album.dict())
		
		# Check callback
		callback = request.GET.get('callback')
		if (callback != None):
			# Stringify albums inside callback function call
			json_data = callback + '(' + json.dumps(albums) + ');'
		else:
			# No callback, stringify with indentation
			json_data = json.dumps(albums, indent=2)
			
		return HttpResponse(json_data, content_type='application/json')
	
	elif request.method == 'HEAD':
		return HttpResponse()
	
	elif request.method == 'POST':
		# Create new album
		artist_id = request.POST.get('artist_id')
		album = request.POST.get('album')
		year = request.POST.get('year')

		if not artist_id or not album:
			# Artist_id and album name required
			return HttpResponse(status=400)
		if not year:
			year = None
		
		# Find artist
		try:
			artist = Artist.objects.get(id=artist_id)
		except Artist.DoesNotExist:
			raise Http404('Artist with ID ' + artist_id + ' does not exist.')
		
		Album.objects.create(name=album, artist=artist, year=year)
		return HttpResponse(status=201)
	
	return HttpResponse(status=405)

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
	
	
	return HttpResponse(id, content_type='application/json')

def tracks(request):
	# Examine request
	if request.method == 'GET':
		# Get all tracks
		tracks = []
		for track in Track.objects.all():
			tracks.append(track.dict())
		
		# Check callback
		callback = request.GET.get('callback')
		if (callback != None):
			# Stringify albums inside callback function call
			json_data = callback + '(' + json.dumps(tracks) + ');'
		else:
			# No callback, stringify with indentation
			json_data = json.dumps(tracks, indent=2)
			
		return HttpResponse(json_data, content_type='application/json')
	
	elif request.method == 'HEAD':
		return HttpResponse()
	
	elif request.method == 'POST':
		# Create new track
		album_id = request.POST.get('album_id')
		track = request.POST.get('track')
		duration = request.POST.get('duration')
		
		if not album_id or not track:
			# Album_id and track name required
			return HttpResponse(status=400)
		# Reormat duration
		if not duration:
			duration = None
		else:
			duration = timedelta(seconds=int(duration))
		
		# Find album
		try:
			album = Album.objects.get(id=album_id)
		except Album.DoesNotExist:
			raise Http404('Album with ID ' + album_id + ' does not exist.')
		
		Track.objects.create(name=track, album=album, duration=duration)
		return HttpResponse(status=201)
	
	return HttpResponse(status=405)
	
def search(request):
	# 501 Not Implemented
	return HttpResponse(status=501)
