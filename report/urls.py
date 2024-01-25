from report.views import ReportUserView
from django.urls import path

# v1/report/
urlpatterns = [
    # v1/report/<social_user_id>/user/
    path("<str:social_user_id>/user/", ReportUserView.as_view()),
]
