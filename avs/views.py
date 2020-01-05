from django.shortcuts import render
from avs.models import YoutubeVideo
import requests, json
from os import environ
# Create your views here.
from threading import Thread as thr
import urllib.request

vs = YoutubeVideo.objects.all()
vsc = vs.count()

def index(request):
    return render(request, 'avs/index.html', {
        'videos': vs,
        'count': vsc
    })

videos = []
url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=UUZu-JP1plc5VlBQ1d-eG7cQ&key='+environ.get('YT_KEY')

def fill_data(e):

    print(f'The video of {e[0]} id has {e[1]} name, published at {e[2][:10]}.')
    st = ytstats(e[0])
    game = [0,0,0]
    if st[0] == '2011':
        parsing = ytgetgame(e[0])
        if parsing:
            game = parsing
            print(f'The game is {game[0]}. {game[1]}!\n')
    else:
        print('')
        
    # id, name, date, like, dislike, views, comments, duration, category, game, thumbnail, gamepic


    v = YoutubeVideo(youtube_id=e[0], name=e[1], date=e[2][:10], category=st[0], duration=st[1], comments=st[2],
                        dislike=st[4], like=st[5], views=st[3], game=game[0], yt_thumbnail=e[3],
                        game_yt_pic=game[2], game_year=game[1])
    v.save()

def ytgetvideos(url, headers, count):

    r = requests.get(url, headers)

    while count:

        video = []
        youtube_id = ''
        pub_date = ''
        name = ''
        thumbnail_high = ''

        for e in r.json()['items']:
            if count:
                count-=1
                print(e)
                youtube_id = e['snippet']['resourceId']['videoId']
                name = e['snippet']['title']
                pub_date = e['snippet']['publishedAt']
                thumbnail = e['snippet']['thumbnails']['high']['url']
                print(youtube_id, name)
                video = [youtube_id, name, pub_date, thumbnail]
                videos.append(video)
                thr(target=fill_data, args=(video,)).start()

        if 'nextPageToken' in r.json():

            pageToken = r.json()['nextPageToken']
            print(pageToken)
            headers = {'pageToken': pageToken}
            ytgetvideos(url, headers, count)


        break


def ytgetgame(youtube_id):

    url = 'https://www.youtube.com/watch?v=' + youtube_id

    r = requests.get(url)
    # s = BeautifulSoup(r.text, 'html.parser')
    print(r.text)
    p = r.text.find('metadataWithImageRowRenderer')
    if p==-1:
        return 0
    p1 = r.text[p:p+1001]
    p2 = p1.find('contents')+30
    p3 = p1[p2:]
    name = p3[:p3.find('"')-1]
    point = p1.find('thumbnail')
    year = p1[point-11:point-7]
    pic = p1[point+44:point+134]

    print(year, pic)
    return name, year, pic

def ytstats(id):

    headers = {}
    url = f'''https://www.googleapis.com/youtube/v3/videos?id={id}&key={environ.get('YT_KEY')}&part=snippet,contentDetails,statistics,status'''

    r = requests.get(url, headers)
    r = r.json()['items'][0]
    dur = r['contentDetails']['duration']
    like = r['statistics']['likeCount']
    views = r['statistics']['viewCount']
    dislike = r['statistics']['dislikeCount']
    commentscount = r['statistics']['commentCount']
    categoryid = r['snippet']['categoryId']

    print(f'It has {like} likes, {dislike} dislikes, {views} views, {commentscount} comments, duraion is {dur[2:]} and category is {categoryid}.')
    return(categoryid, dur[2:], commentscount, views, dislike, like)

# YoutubeVideo.objects.all().delete()
# thr(target=ytgetvideos, args=(url, {}, 999)).start()
# print(len(videos), videos[0], '\n')

def get_yttn(link, id):
    print(link, id)
    urllib.request.urlretrieve(link, f"../media/yttn/{id}yttn.jpg")

# for e in vs:
#     thr(target=get_yttn, args=(e.yt_thumbnail, e.id)).start()