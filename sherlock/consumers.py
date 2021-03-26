import json
import time
import datetime
import asyncio
from asgiref.sync import sync_to_async
from django.core import serializers
from channels.generic.websocket import AsyncWebsocketConsumer
from sherlock.models import Packet
from .socket_sniffer import SocketSniffer

sniffer = SocketSniffer()

class NetworkDataConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        # Accept the connection
        await self.accept()

        self.connected = True

        # While we are connected...
        while self.connected:
            # Sleep for one second(s)
            await asyncio.sleep(0.01)

            # Get packets that have appeared recently
            # packet = await self.get_packets()
            packet = sniffer.receive_packet()
            if packet is not None:
                packets = []
                packets.append(packet)
                
                # Save the packet to the database
                self.save_packets(packet)

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
    def get_packets(self):
        return sniffer.receive_packet()

    @sync_to_async
    def save_packets(self, packet):
        try:
            # Save the packet to the database
            packet.save()
        except Exception as e:
            print("Failed to save the packet: {}", e)

    @sync_to_async
    def serialize_packets(self, packets):
        return serializers.serialize("json", packets)