from django.urls import path

from news.views import NewsView, NewsHeadlinesView

# v1/news/
urlpatterns = [
    # v1/news/
    path("", NewsView.as_view()),
    # v1/news/headlines/
    path("headlines/", NewsHeadlinesView.as_view()),
]
