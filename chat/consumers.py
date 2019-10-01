from google.cloud import texttospeech
from google.cloud import storage
from googleapiclient.discovery import build
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncConsumer, SyncConsumer
import json, asyncio, time, uuid#, colorama
from googleapiclient.discovery import build
from threading import Thread as thr
from os import environ
from time import sleep

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from google.cloud.texttospeech import enums

from chat.models import TwitchIrcChannel, GttsVoiceLanguage, ChatMessage, ChatUser

channel_layer = get_channel_layer()

HOST = 'irc.chat.twitch.tv'
PORT = 6667
PASS = environ.get('TW_PASS')
NICK = 'sn_b0t'

voices_list = []

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

def tts(vcmessage, name, voice_preset):

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


async def irc():

    print('startirc')
    reader, writer = await asyncio.open_connection(HOST, PORT)
    writer.write('PASS {}\r\n'.format(PASS).encode("utf-8"))
    writer.write('NICK {}\r\n'.format(NICK).encode("utf-8"))
    for channel in TwitchIrcChannel.objects.all():
        join_message = 'JOIN #'+channel.username+'\r\n'
        writer.write(join_message.encode("utf-8"))
    while True:
        data = await reader.read(1024)
        message = data.decode()
        print(message)
        if message == "PING :tmi.twitch.tv\r\n":
            writer.write('PONG :tmi.twitch.tv\r\n'.encode("utf-8"))
        await tw_irc_type(message)


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

thr(target=list_voices).start()
thr(target=ytchat).start()
asyncio.ensure_future(irc())

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

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

        # if message == '!!':
        #     if not self.irc_on and self.room_name == 'lobby':
        #         self.irct = asyncio.create_task(self.irc())
        #         asyncio.create_task(ytchat())
        #         print(self.irct)
        #         self.irc_on = 1
        # if message == '!!!':
        #      self.irct.cancel()
        #      print(self.irct)
        #      self.irc_on = 0
        
        # Send message to WebSocket
        if not message.startswith("!"):
            await self.send(text_data=json.dumps({
                'message': message,
            }))

client = ChatConsumer('test')
print(client)

class ChattyBotConsumer(SyncConsumer):

    def telegram_message(self, message):
        """
        Simple echo handler for telegram messages in any chat.
        """
        print(987987)
    async_to_sync(channel_layer.send)('telegram', {
            "type": "telegram.message",
            "text": "You said: ",
        
        })

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
            thr(target=tts, args=(vcmessage, name, voice )).start()
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