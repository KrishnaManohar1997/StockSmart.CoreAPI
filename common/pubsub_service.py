from redis import StrictRedis
from django.conf import settings

redis_instance = StrictRedis(
    host=settings.REDIS_URL.lstrip("redis://"),
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
)
pubsub = redis_instance.pubsub()


class PubsubService:
    def get_pubsub_instance(self):
        return redis_instance

    def get_subscriber(self, topic):
        pubsub.subscribe(topic)
        return pubsub
