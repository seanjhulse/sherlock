import json
import time
import datetime
import asyncio
from asgiref.sync import sync_to_async
from django.core import serializers
from channels.generic.websocket import AsyncWebsocketConsumer
from sherlock.models import Packet
from .socket_sniffer import SocketSniffer
from threading import Thread

sniffer = SocketSniffer()
class NetworkDataConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        # Accept the connection
        await self.accept()

        self.connected = True
        
        thread1 = Thread(target=sniffer.sniff_packets)
        thread2 = Thread(target=sniffer.sniff_packets)
        thread1.start()
        thread2.start()

        while self.connected:
            # Sleep for one second(s)
            # await asyncio.sleep(0.1)
            
            # Get packets that have appeared recently
            packet = sniffer.get_packets()

            if packet:
                
                await self.save_packet(packet)

                # Serialize the packets to JSON data
                json_packets = await self.serialize_packets([packet])

                # Send the packets as a JSON object ("message": [Array of Packets])
                await self.send(text_data=json.dumps({
                    "message": json_packets
                }))

        thread1.join()
        thread2.join()

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
    def save_packets(self, packets):
        # Save the packet to the database
        for packet in packets:
            try:
                # Save the packet to the database
                packet.save()
            except Exception as e:
                print("Failed to save the packet: {}", e)\
    
    @sync_to_async
    def save_packet(self, packet):
        try:
            # Save the packet to the database
            packet.save()
        except Exception as e:
            print("Failed to save the packet: {}", e)

    @sync_to_async
    def get_packets(self):
        return sniffer.get_packets()

    @sync_to_async
    def serialize_packets(self, packets):
        return serializers.serialize("json", packets)