from django.urls import path

from user.views import UserLoginView

urlpatterns = [
    # User Login View
    path("login/", UserLoginView.as_view()),
]
