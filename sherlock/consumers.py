import json
import time
from channels.generic.websocket import WebsocketConsumer

class NetworkDataConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.connected = True

        data = 0
        while self.connected:
            print("sending data: %s", data)
            time.sleep(1)
            self.send(text_data=json.dumps({
                'message': data
            }))
            data += 1

    def disconnect(self, close_code):
        self.connected = False
        print("\ndisconnected from network stream\n")
        pass

    def receive(self, text_data):
        pass
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        # self.send(text_data=json.dumps({
        #     'message': message
        # }))