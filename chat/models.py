import datetime
from django.db import models

class ChatUser(models.Model):
	username = models.CharField(max_length=20)
	origin = models.CharField(max_length=20)
	origin_id = models.CharField(max_length=20)

class GttsVoiceLanguage(models.Model):
	language = models.CharField(max_length=10)

class TwitchIrcChannel(models.Model):
	username = models.CharField(max_length=20)
	def __str__(self):
		return self.username

class ChatMessage(models.Model):
	remote_channel = models.ForeignKey(TwitchIrcChannel, on_delete=models.CASCADE, blank=True, null=True)
	user = models.ForeignKey(ChatUser, on_delete=models.CASCADE, blank=True, null=True)
	# language = models.ForeignKey(GttsVoiceLanguage, on_delete=models.CASCADE, blank=True, null=True)
	language = models.CharField(max_length=15, default="", blank=True, null=True)
	message_type = models.CharField(max_length=10, default="", blank=True, null=True)
	speech_url = models.URLField(default="", blank=True, null=True)
	text = models.CharField(max_length=2000)
	pub_date = models.DateTimeField('date', auto_now_add=True)
	def __str__(self):
		return self.text
