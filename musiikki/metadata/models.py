from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['name']

class Album(models.Model):
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    year = models.IntegerField()
    
    class Meta:
        ordering = ['year', 'name']

class Track(models.Model):
    name = models.CharField(max_length=255)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracklist')
    duration = models.DurationField()
    
    class Meta:
        ordering = ['name']