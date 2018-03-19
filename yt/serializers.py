from rest_framework import serializers
from yt.models import YoutubeStat

class YoutubeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YoutubeStat
        fields = ('subs', 'views', 'status')