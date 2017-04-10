from django.shortcuts import render
from django.http import HttpResponse, Http404, QueryDict
from django.db.models.query import QuerySet
from django.db.models.functions import Lower

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
		return JSONResponse(artist, request.GET.get('callback'))
	
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
		if 'artist' in patch.keys():
			artist.name = patch.get('artist')
			modified = True
		
			if not artist.name:
				# Required field is empty, bad request
				return HttpResponse(status=400)
			
		if 'genre' in patch.keys():
			artist.genre = patch.get('genre')
			modified = True
			
			if not artist.genre:
				# Optional field is empty, set to None
				artist.genre = None
		
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
		artists = Artist.objects.all().order_by(Lower('name'))
		return JSONResponse(artists, request.GET.get('callback'))
	
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
		
		try:
			artist = Artist.objects.create(name=artist, genre=genre)
		except ValueError:
			# Bad values
			HttpResponse(status=400)
		
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
		return JSONResponse(album, request.GET.get('callback'))
	
	elif request.method == 'HEAD':
		return HttpResponse()
	
	elif request.method == 'POST':
		# Conflict, album already exists
		return HttpResponse(status=409)
		
	elif request.method == 'PUT':
		put = QueryDict(request.body)
		# TODO: Replace ad hoc implementation
		name = put.get('album')
		#artist_id = put.get('artist_id')
		if not name:
			return HttpResponse(status=400)
		
		year = put.get('year')
		if not year:
			year = None
		
		# Assign values
		album.name = name
		album.year = year
		try:
			album.save()
		except ValueError:
			return HttpResponse(status=400)
		
		return HttpResponse()
	
	elif request.method == 'PATCH':
		patch = QueryDict(request.body)
		modified = False
		# TODO: Dynamic implementation
		if 'album' in patch.keys():
			album.name = patch.get('album')
			modified = True
		
		if 'year' in patch.keys():
			album.year = patch.get('year')
			modified = True
		
		if modified:
			try:
				album.save()
			except ValueError:
				return HttpResponse(status=400)
		
		return HttpResponse()
	
	elif request.method == 'DELETE':
		# Delete album
		album.delete()
		return HttpResponse()
	
	return HttpResponse(status=405)

def albums(request):
	# Examine request
	if request.method == 'GET':
		# Order by lower case name and artist
		albums = Album.objects.all().order_by(Lower('name'), Lower('artist__name'))
		return JSONResponse(albums, request.GET.get('callback'))
	
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
		
		try:
			# Save album
			album = Album.objects.create(name=album, artist=artist, year=year)
		except ValueError:
			# Bad values
			return HttpResponse(status=400)
		
		if not album:
			# Album was not created
			return HttpResponse(status=507)
		
		response = HttpResponse(status=201)
		response['location'] = album.id
		return response
	
	elif request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
		return HttpResponse(status=404)
	
	return HttpResponse(status=405)

def track(request, id):
	# Find track
	try:
		track = Track.objects.get(id=id)
	except Track.DoesNotExist:
		raise Http404('Track with ID ' + id + ' does not exist.')
	
	# Examine request
	if request.method == 'GET':
		return JSONResponse(track, request.GET.get('callback'))
	
	elif request.method == 'HEAD':
		return HttpResponse()
	
	elif request.method == 'POST':
		# Conflict, track already exists
		return HttpResponse(status=409)
		
	elif request.method == 'PUT':
		put = QueryDict(request.body)
		# TODO: Replace ad hoc implementation
		name = put.get('track')
		#album_id = put.get('album_id')
		if not name:
			return HttpResponse(status=400)
		
		duration = put.get('duration')
		if not duration:
			duration = None
		else:
			try:
				duration = timedelta(seconds=int(duration))
			except ValueError:
				# Unable to convert duration to int
				return HttpResponse(status=400)
		
		# Assign values
		track.name = name
		track.duration = duration
		track.save()
		
		return HttpResponse()
	
	elif request.method == 'PATCH':
		patch = QueryDict(request.body)
		modified = False
		# TODO: Dynamic implementation
		if 'track' in patch.keys():
			track.name = patch.get('track')
			modified = True
		
		if 'duration' in patch.keys():
			try:
				track.duration = timedelta(seconds=int(patch.get('duration')))
				modified = True
			except ValueError:
				# Unable to convert duration to int
				return HttpResponse(status=400)
		
		if modified:
			track.save()
		
		return HttpResponse()
	
	elif request.method == 'DELETE':
		# Delete track
		track.delete()
		return HttpResponse()
	
	return HttpResponse(status=405)

def tracks(request):
	# Examine request
	if request.method == 'GET':
		# Order by lower case name and artist
		tracks = Track.objects.all().order_by(Lower('name'), Lower('album__artist__name'))
		return JSONResponse(tracks, request.GET.get('callback'))
	
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
		# Reformat duration
		if not duration:
			duration = None
		else:
			try:
				duration = timedelta(seconds=int(duration))
			except ValueError:
				return HttpResponse(status=400)
		
		# Find album
		try:
			album = Album.objects.get(id=album_id)
		except Album.DoesNotExist:
			raise Http404('Album with ID ' + album_id + ' does not exist.')
		
		track = Track.objects.create(name=track, album=album, duration=duration)
		if not track:
			# Track was not created
			return HttpResponse(status=507)
		
		response = HttpResponse(status=201)
		response['location'] = track.id
		return response
	
	elif request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE':
		return HttpResponse(status=404)
	
	return HttpResponse(status=405)
	
def search(request):
	keywords = {}
	# Filter out empty values
	for key in request.GET:
		value = request.GET[key]
		if value:
			keywords[key] = value
	print(keywords)
	# Access descendants' attributes in hierarchy by syntax: child__grandchild__attribute
	hierarchy_prefix = ''
	# Store the actual search results
	data = []
	# Has search results been stored to data variable
	data_filled = False
	
	if data_filled:
		# Append to filter hierarchy prefix
		hierarchy_prefix += 'track__'
		
	if 'track' in keywords:
		if not data_filled:
			# If data variable is not filled with any search results, fill it
			# withdata with all tracks
			data = Track.objects.all()
			# Sort data
			data = data.order_by(Lower('name'), Lower('album__artist__name'),
				Lower('album__artist__genre'), Lower('album__name'))
			data_filled = True
		# Filter by track title
		# '__icontains' = the attribute contains the value and comparison is
		# case insensitive
		data = data.filter(**{hierarchy_prefix + 'name__icontains': keywords['track']})
	
	if data_filled:
		hierarchy_prefix += 'album__'
	
	if 'album' in keywords:
		if not data_filled:
			# Fill data with albums
			data = Album.objects.all()
			# Sort data
			data = data.order_by(Lower('name'), Lower('artist__name'), Lower('artist__genre'))
			data_filled = True
		# Filter by album title
		data = data.filter(**{hierarchy_prefix + 'name__icontains': keywords['album']})
	
	if data_filled:
		hierarchy_prefix += 'artist__'
	
	if 'artist' in keywords:
		if not data_filled:
			# Fill data with artists
			data = Artist.objects.all()
			# Sort data
			data = data.order_by(Lower('name'), Lower('genre'))
			data_filled = True
		# Filter by artist name
		data = data.filter(**{hierarchy_prefix + 'name__icontains': keywords['artist']})
		
	if 'genre' in keywords:
		if not data_filled:
			# Fill data with artists
			data = Artist.objects.all()
			# Sort data
			data = data.order_by(Lower('name'), Lower('genre'))
			data_filled = True
		# Filter by genre
		data = data.filter(**{hierarchy_prefix + 'genre__icontains': keywords['genre']})
	
	return JSONResponse(data, request.GET.get('callback'))

# Returns QuerySet in a HttpResponse as JSON data
# If callback function name is given
def JSONResponse(query_set, callback=None):
	try:
		try:
			# Get all items
			data = []
			for item in query_set:
				try:
					data.append(item.dict())
				except AttributeError:
					#item has no attribute dict
					data.append(item)
		except TypeError:
			# query_set is not iterable
			try:
				data = query_set.dict()
			except AttributeError:
				#query_set has no attribute dict
				data = query_set
		
		# Check callback
		if (callback != None):
			# Stringify list inside callback function call
			json_data = callback + '(' + json.dumps(data) + ');'
		else:
			# No callback, stringify with indentation
			json_data = json.dumps(data, indent=2)
			
		return HttpResponse(json_data, content_type='application/json')
	except:
		return HttpResponse(status=500)