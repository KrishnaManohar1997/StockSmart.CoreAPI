from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        self.user = user
        # When Token is Invalid User will be None
        if user is None:
            await self.disconnect(4888)
        else:
            self.room_group_name = str(user.id)
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if self.user != None:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
            if settings.DEBUG:
                await self.close()
        else:
            await self.accept()
            await self.close(close_code)

    # Receive message from the group
    async def channel_message(self, event):
        # Send message to WebSocket
        await self.send_json({"data": event.get("data")})

    async def receive(self, text_data):
        await self.send_json({"data": "connected"})

        # Driver Code
        # await self.channel_layer.group_send(
        #     self.room_group_name, {"type": "channel_message", "message": text_data}
        # )
