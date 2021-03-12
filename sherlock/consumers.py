import json
import time
import datetime
import asyncio
from asgiref.sync import sync_to_async
from django.core import serializers
from channels.generic.websocket import AsyncWebsocketConsumer
from sherlock.models import Packet

class NetworkDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the connection
        await self.accept()

        self.connected = True

        # While we are connected...
        while self.connected:

            # Sleep for one second(s)
            await asyncio.sleep(0.5)

            # Get packets that have appeared 1 second(s) ago
            packets = await self.get_packets(1)

            # Serialize the packets to JSON data
            json_packets = await self.serialize_packets(packets)

            # Send the packets as a JSON object ("message": [Array of Packets])
            await self.send(text_data=json.dumps({
                "message": json_packets
            }))

    async def disconnect(self):
        self.connected = False
        print("\nDisconnected from network stream")

    async def receive(self):
        pass
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

    @sync_to_async
    def get_packets(self, seconds_ago):
        # Creates a datetime "seconds_ago" seconds in the past
        created_time = datetime.datetime.now() - datetime.timedelta(seconds=seconds_ago)

        # Gets all Packets which were created > created_time (seconds ago)
        packets = Packet.objects.filter(pub_date__gt=created_time)
        return packets

    @sync_to_async
    def serialize_packets(self, packets):
        return serializers.serialize("json", packets)