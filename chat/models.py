import datetime
from django.db import models


class ChatUser(models.Model):
	username = models.CharField(max_length=20)
	origin = models.CharField(max_length=20)
	origin_id = models.CharField(max_length=20)

class GttsVoiceLanguage(models.Model):
	language = models.CharField(max_length=10)

class ChatMessage(models.Model):
	user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
	language = models.ForeignKey(GttsVoiceLanguage, on_delete=models.CASCADE)
	message_type = models.CharField(max_length=10)
	question_text = models.CharField(max_length=20)
	pub_date = models.DateTimeField('date published')
	def __str__(self):
		return self.question_text
