from __future__ import absolute_import, unicode_literals
import time, requests
from celery import shared_task
from tw.models import TwitchStat
from mysite.settings import TwitchClientID

@shared_task
def add(x, y):
    return x + y

@shared_task
def tw():
	s = TwitchStat.objects.get(name='mainstats')

	url_v = 'https://api.twitch.tv/helix/users?login=sunraylmtd'
	url_s = 'https://api.twitch.tv/helix/streams?user_login=sunraylmtd'
	url_f = 'https://api.twitch.tv/helix/users/follows?to_id=137288201'

	headers = {'Client-ID': TwitchClientID}

	rv = requests.get(url_v, headers=headers)
	rs = requests.get(url_s, headers=headers)
	rf = requests.get(url_f, headers=headers)
	views = rv.json()['data'][0]['view_count']
	stat = rs.json()['data']
	flow = rf.json()['total']

	if stat:
	    s.status = True
	else:
	    s.status = False
	s.views = views
	s.subs = flow
	print(s.status)
	print(flow)
	print(views)

	s.save()
	return