from django.db import models

# Create your models here.

class YoutubeStat(models.Model):

    subs = models.PositiveSmallIntegerField()
    views = models.IntegerField()
    status = models.BooleanField()
    name = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class YoutubeVideo(models.Model):

	views = models.PositiveSmallIntegerField(blank=True)
	youtube_id = models.CharField(max_length=16)
	name = models.CharField(max_length=100)
	game = models.CharField(max_length=600, blank=True)
	game_yt_pic = models.CharField(max_length=600, blank=True)
	game_yt_url = models.CharField(max_length=600, blank=True)
	date = models.DateField(blank=True)
	def __str__(self):
		return self.name
