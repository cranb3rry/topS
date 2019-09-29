from django.contrib import admin

# Register your models here.

from .models import TwitchIrcChannel, ChatMessage

class ChatMessageAdmin(admin.ModelAdmin):

    list_display = ('text', 'pub_date')
    list_filter = ['pub_date']

admin.site.register(TwitchIrcChannel)
admin.site.register(ChatMessage, ChatMessageAdmin)