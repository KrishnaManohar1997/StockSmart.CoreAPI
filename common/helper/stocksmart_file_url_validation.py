from django.conf import settings


def is_stocksmart_file_url(url: str):
    return url.startswith(settings.S3_URL) or url.startswith(
        "https://media.giphy.com/media"
    )
