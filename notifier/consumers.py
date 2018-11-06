from channels.generic.websocket import AsyncJsonWebsocketConsumer
#from channels.exceptions import StopConsumer
import asyncio
import logging
import sys, time

passw = 'PASS oauth:17gvf82i0pjx40ffg5qdilvnm8rzem\r\n'.encode()
nick = 'NICK sn_b0t\r\n'.encode()
channels = ['sn_b0t', 'sunraylmtd', 'f0ck_the_system', 'mangal__official',
    'kolya_incorporated']

login = [
    passw,
    nick
]

cache = []

SERVER_ADDRESS = ('irc.chat.twitch.tv', 6667)

class EchoConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        await self.accept()
        #while True:
        await self.send_json('1')
        await asyncio.sleep(1)
        await self.send_json('2')
        await asyncio.sleep(1)

        # reader, writer = await asyncio.open_connection(*SERVER_ADDRESS)

        # for msg in login:
        #     writer.write(msg)
        #     #log.debug('sending {!r}'.format(msg))
        # for channel in channels:
        #     join_message = 'JOIN #'+channel+'\r\n'
        #     writer.write(join_message.encode("utf-8"))
        # while True:
        #     data = await reader.read(1024)
        #     print(data)

    async def disconnect(self, close_code):
        print(close_code)

        # async def receive(self, event):
        #     await self.send({
        #         "type": "websocket.send",
        #         "text": event["text"],
        #     })
        # 