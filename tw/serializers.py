from django.contrib.auth.models import User, Group
from rest_framework import serializers
from tw.models import TwitchStat


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class TwitchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TwitchStat
        fields = ('subs', 'views', 'status')