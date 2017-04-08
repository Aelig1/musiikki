from django.db import models

class Artist(models.Model):
	name = models.CharField(max_length=255)
	genre = models.CharField(max_length=255, null=True, blank=True)
	    
	class Meta:
		ordering = ['name']
	
	# Reformat Artist into a json serializable dict with given fields.
	def dict(self, fields=['id', 'name', 'genre', 'albums']):
		dict = {}
		
		for field in fields:
			# Specify formatting for albums
			if field == 'albums':
				albums = []
				for album in self.albums.all():
					albums.append( album.dict(['id', 'name', 'year']) )
				dict['albums'] = albums
			# Default
			else:
				try:
					dict[field] = getattr(self, field)
				except AttributeError:
					pass

		return dict

class Album(models.Model):
	name = models.CharField(max_length=255)
	artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
	year = models.IntegerField()
   
	class Meta:
		ordering = ['year', 'name']
	
	# Reformat Album into a json serializable dict with given fields.
	def dict(self, fields=['id', 'name', 'artist', 'year', 'tracklist']):
		dict = {}
		
		for field in fields:
			# Specify formatting for artist
			if field == 'artist':
				dict[field] = self.artist.dict(['id', 'name'])
			# Specify formatting for tracks
			elif field == 'tracklist':
				tracklist = []
				# Order by track id because track number isn't included in the data yet
				for track in self.tracklist.all().order_by('id'):
					tracklist.append( track.dict(['id', 'name']) )
				dict[field] = tracklist
			# Default
			else:
				try:
					dict[field] = getattr(self, field)
				except AttributeError:
					pass

		return dict

class Track(models.Model):
	name = models.CharField(max_length=255)
	album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracklist')
	duration = models.DurationField()
	    
	class Meta:
		ordering = ['name']

	# Reformat Track into a json serializable dict with given fields.
	def dict(self, fields=['id', 'name', 'artist', 'album', 'duration']):
		dict = {}
		
		for field in fields:
			# Specify formatting for artist
			if field == 'artist':
				dict[field] = self.album.artist.dict(['id', 'name'])
			# Specify formatting for album
			elif field == 'album':
				dict[field] = self.album.dict(['id', 'name', 'year'])
			# Formatting for duration
			elif field == 'duration':
				dict[field] = '{0}'.format(self.duration)
			# Default
			else:
				try:
					dict[field] = getattr(self, field)
				except AttributeError:
					pass

		return dict