from django.urls import path

from post.views import PostView

urlpatterns = [
    # Post Creation View
    path("", PostView.as_view()),
]
