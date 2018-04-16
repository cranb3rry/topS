import requests
from bs4 import BeautifulSoup
from yt.models import YoutubeVideo
videos = []

def Ytgetvideos(url, headers):

	r = requests.get(url, headers)

	while True:
		pageToken = r.json()['nextPageToken']
		print(pageToken)
		headers = {'pageToken': pageToken}

		video = []
		youtube_id = ''
		pub_date = ''
		name = ''
		thumbnail_high = ''

		for e in r.json()['items']:
			youtube_id = e['id']['videoId']
			name = e['snippet']['title']
			pub_date = e['snippet']['publishedAt']
			thumbnail_high = e['snippet']['thumbnails']['high']['url']
			print(youtube_id, name.encode('utf-8'))
			video = [youtube_id, name, pub_date, thumbnail_high]
			videos.append(video)

		if len(r.json()['items']) > 0:	
			YtGetVideos(url, headers)
		break

	return videos

def Ytgetgame(youtube_id):

	url = 'https://www.youtube.com/watch?v=' + youtube_id

	r = requests.get(url)
	s = BeautifulSoup(r.text, 'html.parser')

	if len(s.find_all(class_=' yt-uix-sessionlink ')) == 3:

		game_name = s.find_all(class_=' yt-uix-sessionlink ')[1].get_text()
		yt_gaming_url = s.find_all(class_=' yt-uix-sessionlink ')[1]['href']
		try:
			yt_game_img = s.find_all(class_=' yt-uix-sessionlink ')[0].find('img')['src'][2:]
		except TypeError:
			yt_game_img = 'no_image'

		return game_name, yt_gaming_url, yt_game_img

	if len(s.find_all(class_=' yt-uix-sessionlink ')) == 1:

		return ' no picture'

	return 'not a game'

def Ytapplygame(ids):
	for e in ids:
		stats = Ytgetgame(e)
		v = YoutubeVideo.objects.get(youtube_id=e)
		if stats[2] not in ['t','o']:
			v.game = stats[0]
		
			v.game_yt_pic = stats[2]
	
			v.game_yt_url = stats[1]
			print(v.id)
			v.save()
		else:
		    v.game = ''
		    v.game_yt_url = ''
		    v.game_yt_pic = ''
		    v.save()
		pass	