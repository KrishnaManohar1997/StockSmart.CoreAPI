from abc import ABC, abstractmethod


class APIResponseHandler(ABC):
    @staticmethod
    @abstractmethod
    def handle_response(response):
        pass
