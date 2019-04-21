

from channels.generic.websocket import AsyncWebsocketConsumer
import json, asyncio, time#, colorama
from googleapiclient.discovery import build

HOST = 'irc.chat.twitch.tv'
PORT = 6667
PASS = 'oauth:17gvf82i0pjx40ffg5qdilvnm8rzem'
NICK = 'sn_b0t'
irc_channels = ['sn_b0t', 'sunraylmtd', 'f0ck_the_system', 'mangalebalo',
    'kolya_incorporated', 'xoaliro']

def tw_irc_format(message, message_type):
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
        

    if message_type == 'JOIN':
        channel = message[message.find('#'):].split()[0]
        # print(Fore.WHITE+'Join', Fore.MAGENTA+channel)

    #if message_type == 'unknown':

        #print(Fore.WHITE+message)

    #ukr(channel, message)

    return

def tw_irc_type(message):

    message_type = 'unknown'

    # keep PRIVMSG last to overwrite user input
    known_types = ['JOIN', 'PING', 'PRIVMSG']

    for kt in known_types:
        if kt in message:
            message_type = kt

    return message_type

# class VcmConsumer(AsyncWebsocketConsumer):

#     def connect(self):
#         self.username = "Anonymous"
#         self.accept()
#         self.send(text_data="[Welcome %s!]" % self.username)

#     def receive(self, *, text_data):
#         if text_data.startswith("/name"):
#             self.username = text_data[5:].strip()
#             self.send(text_data="[set your username to %s]" % self.username)
#         else:
#             self.send(text_data=self.username + ": " + text_data)

#     def disconnect(self, message):
#         pass

service = build('youtube', 'v3')
waittime = 30000

logged_ids = []
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

async def log_messages(message, id):
    if id not in logged_ids:
        print(message)
        await channel_layer.group_send(
                'chat_lobby',
            {
                'type': 'chat_message',
                'message': message[4]+': '+message[1],
            }
        )
        logged_ids.append(id)


async def ytchat():
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
            await log_messages(message, message[0])

        await asyncio.sleep(waittime/1000)


class ChatConsumer(AsyncWebsocketConsumer):

    irc_on = 0

    async def irc(self):

        print('startirc')
        reader, writer = await asyncio.open_connection(HOST, PORT)
        writer.write('PASS {}\r\n'.format(PASS).encode("utf-8"))
        writer.write('NICK {}\r\n'.format(NICK).encode("utf-8"))
        for channel in irc_channels:
            join_message = 'JOIN #'+channel+'\r\n'
            writer.write(join_message.encode("utf-8"))
        while True:
            data = await reader.read(1024)
            message = data.decode()
            print(message)
            if message == '':
                self.irct.cancel()
                print('CANSELED')
                self.irct = asyncio.create_task(self.irc())
            if message == "PING :tmi.twitch.tv\r\n":
                writer.write('PONG :tmi.twitch.tv\r\n'.encode("utf-8"))

            # messages = message.splitlines()
            # for message in messages:
            #     message_type = tw_irc_type(message)
            # tw_irc_format(message, message_type)

            # Send message to room group
            #await self.chat_message({'type': 'chat_message', 'message': message})
            await self.channel_layer.group_send(
                'chat_lobby',
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
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

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                }
            )
        if 'vcm' in text_data_json:
            vcm = text_data_json['vcm']
            print(vcm + ' is a voice message')

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        #print(event)
        print(self.scope)
        if message == '!!':
            if not self.irc_on and self.room_name == 'lobby':
                self.irct = asyncio.create_task(self.irc())
                asyncio.create_task(ytchat())
                print(self.irct)
                self.irc_on = 1
        if message == '!!!':
             self.irct.cancel()
             print(self.irct)
             self.irc_on = 0
        # Send message to WebSocket
        if not message.startswith("!"):
            await self.send(text_data=json.dumps({
                'message': message,
            }))