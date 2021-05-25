import json
from channels.generic.websocket import WebsocketConsumer
from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer(
    "test",
    bootstrap_servers=["localhost:9092"],
    value_deserializer=lambda x: loads(x.decode("utf-8")),
)


class PostCreationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json["data"]
        for message in consumer:
            print(message)
            message = message.value
            self.send(text_data=json.dumps({"message": message}))
