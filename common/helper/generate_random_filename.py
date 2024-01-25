import time

from django.utils.crypto import get_random_string


def get_random_file_name():
    return f"{get_random_string()}_{int(time.time())}"
