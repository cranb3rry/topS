from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# @receiver(post_save, sender=User)
# def announce_new_user(sender, instance, created, **kwargs):
# 	if created:
# 		channel_layer = get_channel_layer()
# 		async_to_sync(channel_layer.group_send)(
# 			"gossip", {
# 				"type": "user.gossip",
# 				"event": "New User",
# 				"username": instance.username
# 			}
# 		)



# channel_layer = get_channel_layer()
# async_to_sync(channel_layer.group_send)(
# 	"chat", {
# 		"type": "chat.message",
# 		"text": "1",

# 	}
# )