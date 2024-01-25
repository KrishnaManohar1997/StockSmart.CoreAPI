from django.urls import path

from smallcase.views import (
    SmallcaseListView,
    SmallcaseView,
    UserTransactionView,
    SmallcaseDetailsListView,
)

# v1/smallcase/
urlpatterns = [
    # v1/smallcase/
    path("", SmallcaseListView.as_view()),
    # v1/smallcase/details/
    path("details/", SmallcaseDetailsListView.as_view()),
    # v1/smallcase/transaction/
    path("transaction/", UserTransactionView.as_view()),
    # v1/smallcase/<symbol>/
    path("<str:smallcase_symbol>/", SmallcaseView.as_view()),
]
