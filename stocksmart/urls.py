"""stocksmart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from post.views.leaderboard import LeaderboardView
from user.views import UserLoginView
from user.views.authentication import TwitterClientOauthTokenView, UserSocialAuthView

from .views import SmallcaseAccountLeadView

# Admin Specific Settings
admin.site.site_header = "Stocksmart Admin"
admin.site.site_title = "Stocksmart Admin"
admin.site.index_title = "Welcome to Stocksmart Admin Panel"


urlpatterns = [
    # Uncomment When Needed
    # path("admin/", admin.site.urls),
    path("v1/login/", UserLoginView.as_view()),
    path("v1/leaderboard/", LeaderboardView.as_view()),
    path("v1/users/", include("user.urls")),
    path("v1/report/", include("report.urls")),
    path("v1/smallcase/", include("smallcase.urls")),
    path("v1/stocks/", include("stock.urls")),
    path("v1/posts/", include("post.urls")),
    path("v1/news/", include("news.urls")),
    path("v1/calendar-events/", include("event_calendar.urls")),
    path("v1/watchlist/", include("watchlist.urls")),
    path("v1/notifications/", include("notification.urls")),
    # Customizing Oauth Token to provide user details
    path(
        "auth/twitter/generate-client-oauthtoken", TwitterClientOauthTokenView.as_view()
    ),
    path("auth/convert-token", UserSocialAuthView.as_view()),
    path("auth/", include("drf_social_oauth2.urls", namespace="drf")),
    path("lead/", SmallcaseAccountLeadView.as_view()),
]
