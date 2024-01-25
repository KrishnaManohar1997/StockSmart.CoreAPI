from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class SocketNotificationService:

    __socket_channel_handler = get_channel_layer()

    @staticmethod
    def get_instance():

        """Static Access Method"""
        if SocketNotificationService.__socket_channel_handler == None:
            SocketNotificationService()
        return SocketNotificationService.__socket_channel_handler

    def __init__(self):

        """virtual private constructor"""
        if SocketNotificationService.__socket_channel_handler != None:
            # print("Socket Notification Instance already exists")
            pass
        else:
            SocketNotificationService.__socket_channel_handler = self

    def send_notification(self, user_id, notification_data):
        async_to_sync(self.__socket_channel_handler.group_send)(
            str(user_id),
            {"type": "channel_message", "data": notification_data},
        )
