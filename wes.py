from django.conf import settings

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocksmart.settings")
application = get_wsgi_application()

from stock.services.stock_service import INDEX_AND_TAPE_STOCKS
from common.socket_notification_service import SocketNotificationService


from twelvedata import TDClient

from threading import Thread
import json


from common import PubsubService

from common.constants import PublisherTopic


class SocketPricingService:
    ws = None
    symbols = INDEX_AND_TAPE_STOCKS

    @staticmethod
    def start_ws():
        print(SocketPricingService.symbols)
        SocketPricingService.open_connection()
        print("Websocket Connection is Opened")
        SocketPricingService.ws.connect()
        print("Subscribed to Default Symbols")
        SocketPricingService.ws.subscribe(SocketPricingService.symbols)
        SocketPricingService.ws.keep_alive()

    @staticmethod
    def stop_ws():
        print("Stopping Websocket")
        SocketPricingService.ws.unsubscribe(SocketPricingService.symbols)
        SocketPricingService.ws.disconnect()
        T.stop()

    @staticmethod
    def open_connection():
        td = TDClient(apikey=settings.TWELVE_DATA_API_KEY)

        SocketPricingService.ws = td.websocket(
            symbols=SocketPricingService.symbols,
            on_event=SocketPricingService.on_event,
            log_level="info",
        )

    @staticmethod
    def on_event(e):
        # do whatever is needed with data
        print(e)
        if e["event"] == "price":
            SocketNotificationService().send_notification(
                "5818f6e9-2f1a-47c6-abb7-14dcc844adf6", e
            )

    @staticmethod
    def subscribe_ws(symbol):
        print("Subscribing Websocket ->", symbol)
        symbol = symbol.upper()
        if symbol not in SocketPricingService.symbols:
            SocketPricingService.symbols.append(symbol)
            SocketPricingService.ws.subscribe([symbol])

    @staticmethod
    def unsubscribe_ws(symbol):
        print("UnSubscribing Websocket ->", symbol)
        if symbol in SocketPricingService.symbols:
            SocketPricingService.symbols.remove(symbol)
            SocketPricingService.ws.unsubscribe([symbol])


subscriber = PubsubService().get_subscriber(PublisherTopic.TICKER_QUOTE)
for message in subscriber.listen():
    if message and message.get("type") == "message":
        msg_data = json.loads(message["data"])
        event = msg_data["event"]
        if event == "start":
            # creating a thread T
            T = Thread(target=SocketPricingService.start_ws)
            # starting of thread T
            # That starts the websocket
            T.start()
        elif event == "stop":
            SocketPricingService.stop_ws()
        elif event == "subscribe":
            SocketPricingService.subscribe_ws(msg_data.get("symbol"))
        elif event == "unsubscribe":
            SocketPricingService.unsubscribe_ws(msg_data.get("symbol"))
