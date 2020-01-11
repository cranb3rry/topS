from google.cloud import texttospeech
from google.cloud import storage
from googleapiclient.discovery import build
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncConsumer, SyncConsumer
import json, asyncio, time, uuid#, colorama
from threading import Thread as thr
from os import environ
from time import sleep
import requests
from channels.layers import get_channel_layer
import logging
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from avs.models import YoutubeVideo
from avs.views import ytgetvideos, url
import urllib.request
import aiohttp

from google.cloud.texttospeech import enums

from chat.views import voices_list
from chat.models import TwitchIrcChannel, GttsVoiceLanguage, ChatMessage, ChatUser
import websockets

channel_layer = get_channel_layer()



HOST = 'irc.chat.twitch.tv'
PORT = 6667
PASS = environ.get('TW_PASS')
NICK = 'sn_b0t'

videos = []
url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=UUZu-JP1plc5VlBQ1d-eG7cQ&key='+environ.get('YT_KEY')
print(url)

def list_voices():
    """Lists the available voices."""

    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices()

    for voice in voices.voices:

        # # Display the voice's name. Example: tpc-vocoded
        # print('Name: {}'.format(voice.name))
        ssml_gender = enums.SsmlVoiceGender(voice.ssml_gender)
        # # Display the supported language codes for this voice. Example: "en-US"
        # for language_code in voice.language_codes:
        #     #print('Supported language: {}'.format(language_code))
        #     voices_list.append(language_code)
        voices_list.append([ssml_gender.name, voice.name, voice.language_codes])


        # # Display the SSML Voice Gender
        # print('SSML Voice Gender: {}'.format(ssml_gender.name))

        # # Display the natural sample rate hertz for this voice. Example: 24000
        # print('Natural Sample Rate Hertz: {}\n'.format(
        #     voice.natural_sample_rate_hertz))

@database_sync_to_async
def log_message(message, m_type, url, language):
    m = ChatMessage(text=message, message_type=m_type, speech_url=url, language=language)
    return m.save()

def log_message_sync(message, m_type, url, language):
    m = ChatMessage(text=message, message_type=m_type, speech_url=url, language=language)
    return m.save()

@database_sync_to_async
def clear_ytv():
    print(YoutubeVideo.objects.all())
    YoutubeVideo.objects.all().delete()

def get_yttn(link, id):
    print(link, id)
    urllib.request.urlretrieve(link, f"../media/yttn/{id}yttn.jpg")

def tts(vcmessage, name, voice_preset, donate):
    if not vcmessage:
        vcmessage = ''
    text = vcmessage
    if len(text) > 256:
        text = text[:255]
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    voice = texttospeech.types.VoiceSelectionParams(
        language_code=voice_preset[:-10],
        name=voice_preset)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = client.synthesize_speech(synthesis_input, voice, audio_config)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('snry_bucket')
    blob = bucket.blob(str(uuid.uuid4().hex)+'.mp3')
    blob.upload_from_string(response.audio_content)
    blob.make_public()

    ttsmessage = {'message': [text, blob.public_url], 'type': 'voice_message', 'name': name, 'voice': voice_preset}
    if donate:
        print(donate)
        ttsmessage['donate'] = donate
    #print(ttsmessage)
    async_to_sync(channel_layer.group_send)(                
        'voice', ttsmessage)
    log_message_sync(name+': '+text, 'voice', blob.public_url, voice_preset)
    #return vcmesg.append(ttsmessage)

async def tw_irc_format(message, message_type):
    channel = ''
    t = time.ctime().split()[3]
    if message_type == 'PRIVMSG':
        text = message[message.find(' :')+2:]
        # print(text)
        user = message[1:message.find('!')]
        # print(user)
        channel = message[message.find('#')+1:].split()[0]
        # print(channel)

        # print(Fore.WHITE+t, Fore.CYAN+user+Fore.RED+'@'+
        #     Fore.MAGENTA+channel+':', Fore.YELLOW+text, end=' ')
        await channel_layer.group_send(
        'chat_lobby',
            {
                'type': 'chat.message',
                'message': message,
            }
        )
        if channel == 'sunraylmtd' and text[0:2] == '! ':
            print(text[2:], 'TVC')
            thr(target=tts, args=(text[2:], user, "ru-RU-Wavenet-B", None)).start()

        await log_message(message, 'twitch', '', '')


    if message_type == 'JOIN':
        channel = message[message.find('#'):].split()[0]
        # print(Fore.WHITE+'Join', Fore.MAGENTA+channel)

    #if message_type == 'unknown':

        #print(Fore.WHITE+message)

    #ukr(channel, message)


async def tw_irc_type(message):

    message_type = 'unknown'

    # keep PRIVMSG last to overwrite user input
    known_types = ['JOIN', 'PING', 'PRIVMSG']

    for kt in known_types:
        if kt in message:
            message_type = kt

    await tw_irc_format(message, message_type)

logger = logging.getLogger()
# logger.setLevel(logging.WARNING)
service = build('youtube', 'v3', cache_discovery=False)
waittime = 30000

logged_ids = []

def log_messages(message, id):
    if id not in logged_ids:
        print(message)
        async_to_sync(channel_layer.group_send)(
            'chat_lobby',
            {
                'type': 'chat.message',
                'message': message[4]+': '+message[1],
            }
        )
        logged_ids.append(id)
        log_message_sync(message[4]+': '+message[1], 'youtube', '', '')

def ytchat():
    print('ytchat')
    while True:
        response = service.liveChatMessages().list(liveChatId=
            'EiEKGFVDWnUtSlAxcGxjNVZsQlExZC1lRzdjURIFL2xpdmU',
            part='snippet, id, authorDetails',
            maxResults=500).execute()
        waittime = response['pollingIntervalMillis']
        count = response['pageInfo']['totalResults']

        print(count, waittime)

        for e in response['items']:
            message = [ # id, text, date, channel, name
            e['id'],
            e['snippet']['textMessageDetails']['messageText'],
            e['snippet']['publishedAt'],
            e['authorDetails']['channelId'],
            e['authorDetails']['displayName'],
            ]
            log_messages(message, message[0])

        sleep(waittime/1000)

async def hello():
    await asyncio.sleep(3)
    print('Hello!')
    uri = "ws://localhost/ws/chat/irc/"
    async with websockets.connect(uri) as websocket:

        while True:
            await websocket.recv()

class QwDntConsumer(AsyncConsumer):

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def dnt_main(self, message):
        async with aiohttp.ClientSession() as session:
            url = environ.get('QWU')
            while True:
                html = await self.fetch(session, url)
                msg = json.loads(html)
                if msg['events']:
                    for e in msg['events']:
                        if not e['type'] == 'DONATION':
                            break
                        message = e['attributes']['DONATION_MESSAGE']
                        name = e['attributes']['DONATION_SENDER']
                        donate = [e['attributes']['DONATION_AMOUNT'], e['attributes']['DONATION_CURRENCY']]

                        thr(target=tts, args=(message, name, "ru-RU-Wavenet-B", donate)).start()

                        print(e['donateDatetime'], e['attributes']['DONATION_AMOUNT'], msg, e)
                await asyncio.sleep(2)


class OkChatConsumer(AsyncConsumer):

    switch = 0

    async def ok_ws(self, message):

        if self.switch:
            print(self.switch)
            pass

        self.switch = 1
        uri = "wss://vm.mycdn.me/chat"
        async with websockets.connect(uri) as websocket:
            name = """{"type":"SYSTEM","systemType":"LOGIN","loginString":"cid=1432198192771&uid=56280619395&s=edc6e8c4dc399a2c67d01992e7cb7fdbfdc3eaab","historyCount":5,"donatesHistoryCount":3,"orientationHistory":false,"lite":false,"seq":0,"version":1}"""

            await websocket.send(name)
            # print(f"> {name}")
            while True:
                msg = await websocket.recv()
                print(msg)
                if json.loads(msg)["type"] == 'TEXT':
                    msg = json.loads(msg)
                    await channel_layer.group_send(
                    'chat_lobby',
                        {
                            'type': 'chat.message',
                            'message': '(ok) '+str(msg['userInfo']['firstName'])+' '+
                            str(msg['userInfo']['lastName'])+': '+str(msg['text']),
                        }
                    )

class TwitchChatConsumer(AsyncConsumer):

    switch = 0
    attempts = 0

    async def tw_irc(self, message):

        if self.switch:
            print(self.switch)
            pass

        self.switch = 1

        while True:

            print('startirc')
            reader, writer = await asyncio.open_connection(HOST, PORT)
            writer.write('PASS {}\r\n'.format(PASS).encode("utf-8"))
            writer.write('NICK {}\r\n'.format(NICK).encode("utf-8"))

            for channel in TwitchIrcChannel.objects.all():
                join_message = 'JOIN #'+channel.username+'\r\n'
                writer.write(join_message.encode("utf-8"))
                
            while True:
                data = await reader.read(1024)
                if not data:
                    print('ircnodata')
                    break
                message = data.decode()
                print(message, end='')
                if message == "PING :tmi.twitch.tv\r\n":
                    writer.write('PONG :tmi.twitch.tv\r\n'.encode("utf-8"))
                if 'Слава Україні!' in message:
                    ch = message[message.find('#')+1:].split()[0]
                    writer.write(("PRIVMSG #"+ch+" :Героям слава!\r\n").encode("utf-8"))

                await tw_irc_type(message)
            
            writer.close()
            await writer.wait_closed()
            self.attempts+=1
            print('restart irc')
            if self.attempts>3:
                await asyncio.sleep(30)

class TaskConsumer(AsyncConsumer):

    switch = 0

    async def start_tasks(self, message):
        print(self.switch)
        if not self.switch:
            
            # thr(target=list_voices).start()
            thr(target=ytchat).start()

            self.switch = 1

thr(target=list_voices).start()
async_to_sync(channel_layer.send)("qw",{ "type": "dnt.main",})
async_to_sync(channel_layer.send)("tw",{ "type": "tw.irc",})
async_to_sync(channel_layer.send)("ok",{ "type": "ok.ws",})
async_to_sync(channel_layer.send)("tasks",{ "type": "start.tasks",})


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        print(self.scope)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print(self.room_name, self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(self)
        if self.room_group_name == 'chat_lobby':
            await self.send(text_data=json.dumps({'message': 'Welcome to Chat!'}))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data)
        print(self.room_group_name)
        if 'message' in text_data_json:
            message = text_data_json['message']   

            await log_message(message, '', '', '')

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                }
            )
        if 'vcm' in text_data_json:
            vcm = text_data_json['vcm']
            print(vcm + ' is a voice message')

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        if not message.startswith("!"):
            await self.send(text_data=json.dumps({
                'message': message,
            }))

    def YtGetVideos(self, url, headers, count):

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
                v = YoutubeVideo(youtube_id=youtube_id, name=name, yt_thumbnail=thumbnail_high, date=pub_date[:10])          
                v.save()

            if 'nextPageToken' in r.json():

                pageToken = r.json()['nextPageToken']
                print(pageToken)
                headers = {'pageToken': pageToken}
                self.YtGetVideos(url, headers, count)
            
            break

        return videos

# YoutubeVideo.objects.all().delete()
# thr(target=c1.YtGetVideos, args=(url, {}, 999)).start()

class VcmsgConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.group = 'voice'

        # Join group
        await self.channel_layer.group_add(
            self.group,
            self.channel_name
        )

        await self.accept()
        await self.send(json.dumps({'message': 'Voice Messages, Connected',
            'type': 'greet'}))
        await self.send(json.dumps({'message': str(voices_list),
            'type': 'voices_list'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('voice', self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        name = text_data_json.get("name", "")
        vcmessage = text_data_json.get("vcm", "")
        voice = text_data_json.get("voice", "")
        if vcmessage:
            thr(target=tts, args=(vcmessage, name, voice, None)).start()
        if text_data == '{"ctrl":"skip"}':
            if self.scope['user'].is_superuser:
                await self.channel_layer.group_send(
                    'voice',
                    {
                        'type': 'voice_skip',
                    }
                )

    async def voice_message(self, event):
        
        await self.send(json.dumps(event))

    async def voice_skip(self, event):
         await self.send(json.dumps({'':'','type':'skip'}))
         