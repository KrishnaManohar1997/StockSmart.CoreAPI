import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class PostCreationConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_name = "posts"
        self.room_group_name = "chat_%s" % self.scope["user"].id
        self.channel_name = f"{self.scope['user'].id}.random"
        # print(self.room_group_name, self.channel_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        # message = text_data_json["message"]
        # message = text_data_json

        # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name, {"type": "chat_message", "message": text_data_json}
        # )

        # Send Message to a specific person

        if text_data_json.get("type"):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "message": "connected"},
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                "chat_" + text_data_json["to"],
                {"type": "chat_message", "message": text_data_json["message"]},
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({"message": message}))
