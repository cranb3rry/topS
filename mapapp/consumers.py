from channels.generic.websocket import AsyncWebsocketConsumer
import json, asyncio
from threading import Thread as thr

class MapGetConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        if str(self.user) == 'archie':
            await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            'geo_send',
            {
                    'type': 'geodata',
                    'x': data['x'],
                    'y': data['y'],
                    'z': data['z'],
                    'ln': data['ln'],
                    'lt': data['lt'],
            }
        )

class MapSendConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            'geo_send',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        pass
    # Receive message from WebSocket
    async def receive(self, text_data):
        pass

    async def geodata(self, event):

        await self.send(json.dumps(event))