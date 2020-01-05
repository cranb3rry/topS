from django.db import models

# Create your models here.

class YoutubeVideo(models.Model):

    # id, name, date, like, dislike, views, comments, duration, category, game, thumbnail, gamepic

    category = models.PositiveSmallIntegerField(blank=True)
    duration = models.CharField(max_length=20, blank=True)
    comments = models.PositiveSmallIntegerField(blank=True)
    like = models.PositiveSmallIntegerField(blank=True)
    dislike = models.PositiveSmallIntegerField(blank=True)
    views = models.PositiveSmallIntegerField(blank=True)
    youtube_id = models.CharField(max_length=16)
    name = models.CharField(max_length=600)
    game = models.CharField(max_length=600, blank=True)
    game_year = models.PositiveSmallIntegerField(blank=True)
    game_yt_pic = models.CharField(max_length=600, blank=True)
    yt_thumbnail = models.CharField(max_length=600, blank=True)
    game_yt_url = models.CharField(max_length=600, blank=True)
    date = models.DateField(blank=True)
    def __str__(self):
        return (f'{self.name}, {self.youtube_id}, {self.date}, {self.game}, {self.views}, {self.like}, {self.dislike}, {self.comments}, {self.duration}, {self.category}')