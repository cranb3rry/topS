from __future__ import absolute_import, unicode_literals
import time, requests
from celery import shared_task
from yt.models import YoutubeStat
from mysite.settings import YoutubeAPI

@shared_task
def yt():
	stats = YoutubeStat.objects.get(name='mainstats')

	is_live = 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCZu-JP1plc5VlBQ1d-eG7cQ&type=video&eventType=live'
	remote_stats = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UCZu-JP1plc5VlBQ1d-eG7cQ'


	headers = {'key': YoutubeAPI}

	rl = requests.get(is_live, headers)
	rs = requests.get(remote_stats, headers)

	views = rs.json()['items'][0]['statistics']['viewCount']
	status = rl.json()['pageInfo']['totalResults']
	subs = rs.json()['items'][0]['statistics']['subscriberCount']

	if status:
	    stats.status = True
	else:
	    stats.status = False
	stats.views = views
	stats.subs = subs
	print(stats.status)
	print(subs)
	print(views)

	stats.save()
	return