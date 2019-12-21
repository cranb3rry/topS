import requests, json
from os import environ
# from bs4 import BeautifulSoup
# from yt.models import YoutubeVideo
videos = []
url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=UUZu-JP1plc5VlBQ1d-eG7cQ&key='+environ.get('YT_KEY')

def YtGetVideos(url, headers, count):

	r = requests.get(url, headers)
	
	while count:

		video = []
		youtube_id = ''
		pub_date = ''
		name = ''
		thumbnail_high = ''

		for e in r.json()['items']:
			count-=1
			print(e)
			youtube_id = e['snippet']['resourceId']['videoId']
			name = e['snippet']['title']
			pub_date = e['snippet']['publishedAt']
			thumbnail_high = e['snippet']['thumbnails']['high']['url']
			print(youtube_id, name)
			video = [youtube_id, name, pub_date, thumbnail_high]
			videos.append(video)

		if 'nextPageToken' in r.json():

			pageToken = r.json()['nextPageToken']
			print(pageToken)
			headers = {'pageToken': pageToken}
			YtGetVideos(url, headers, count)
		
		break

	return videos

def Ytgetgame(youtube_id):

	url = 'https://www.youtube.com/watch?v=' + youtube_id

	r = requests.get(url)
	# s = BeautifulSoup(r.text, 'html.parser')

	p = r.text.find('metadataWithImageRowRenderer')
	if not p:
		return None
	p1 = r.text[p:p+1001]
	p2 = p1.find('contents')+30
	p3 = p1[p2:]
	p4 = p3[:p3.find('"')-1]
	return p4

	# if len(s.find_all(class_=' style-scope ytd-rich-metadata-renderer ')) == 3:
		
	# 	game_name = s.find_all(class_=' yt-uix-sessionlink ')[1].get_text()
	# 	yt_gaming_url = s.find_all(class_=' yt-uix-sessionlink ')[1]['href']
	# 	try:
	# 		yt_game_img = s.find_all(class_=' yt-uix-sessionlink ')[0].find('img')['src'][2:]
	# 	except TypeError:
	# 		yt_game_img = 'no_image'

	# 	return game_name, yt_gaming_url, yt_game_img

	# if len(s.find_all(class_=' yt-uix-sessionlink ')) == 1:

	# 	return ' no picture'

	# return 'not a game'

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

YtGetVideos(url, {}, 10)
print(len(videos), "123123123", videos[0])
for e in videos:
	print(Ytgetgame(e[0]))
