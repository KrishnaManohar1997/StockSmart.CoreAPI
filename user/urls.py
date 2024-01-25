from user.views import (
    UserProfileView,
    GenerateUserSmallCaseTokenView,
    GenerateGuestSmallcaseTokenView,
    UpdateUserSmallcaseAuthIdView,
    FollowUserView,
    UnfollowUserView,
    BlockUserView,
    UnblockUserView,
    PublicUserProfileView,
    UsernameAvailabilityView,
    UserFollowersListView,
    UserFollowingListView,
    UserFriendshipView,
    UserSearchView,
    UserFileUploadView,
    UserHoldingsView,
    UserHoldingsWebhookView,
    UserRewardsView,
)
from django.urls import path

# v1/users/
urlpatterns = [
    # v1/users/webhook/update-holdings/
    path("webhook/update-holdings/", UserHoldingsWebhookView.as_view()),
    # v1/users/upload-file/
    path("upload-file/", UserFileUploadView.as_view()),
    # v1/users/me/
    path("me/", UserProfileView.as_view()),
    # v1/users/me/rewards/
    path("me/rewards/", UserRewardsView.as_view()),
    # v1/users/me/holdings/
    path("me/holdings/", UserHoldingsView.as_view()),
    # v1/users/me/friendship/
    path("me/friendship/", UserFriendshipView.as_view()),
    # v1/users/me/generate-smallcase-token/
    path("me/generate-smallcase-token/", GenerateUserSmallCaseTokenView.as_view()),
    # v1/users/guest/generate-smallcase-token/
    path("guest/generate-smallcase-token/", GenerateGuestSmallcaseTokenView.as_view()),
    # v1/users/me/update-smallcase-auth-id/
    path("me/update-smallcase-auth-id/", UpdateUserSmallcaseAuthIdView.as_view()),
    # v1/users/search/
    path("search/", UserSearchView.as_view()),
    # v1/users/<username>/
    path("<str:username>/", PublicUserProfileView.as_view()),
    # v1/users/<username>/is-available/
    path("<str:username>/is-username-available/", UsernameAvailabilityView.as_view()),
    # v1/users/<social_user_id>/follow/
    path("<str:social_user_id>/follow/", FollowUserView.as_view()),
    # v1/users/<social_user_id>/followers/
    path("<str:social_user_id>/followers/", UserFollowersListView.as_view()),
    # v1/users/<social_user_id>/following/
    path("<str:social_user_id>/following/", UserFollowingListView.as_view()),
    # v1/users/<social_user_id>/unfollow/
    path("<str:social_user_id>/unfollow/", UnfollowUserView.as_view()),
    # v1/users/<social_user_id>/block/
    path("<str:social_user_id>/block/", BlockUserView.as_view()),
    # v1/users/<social_user_id>/unblock/
    path("<str:social_user_id>/unblock/", UnblockUserView.as_view()),
]
