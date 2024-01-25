from django.urls import path

from post.views import (
    CommentPostView,
    CreatePostView,
    TickerPostFeedView,
    ReactPostView,
    ReactCommentView,
    CommentFeedView,
    PostURLView,
    UserPostsView,
    PostReactionsView,
    CommentReactionsView,
    DeletePostView,
    DeleteCommentView,
    ExplorePostView,
)

# v1/posts/
urlpatterns = [
    # v1/posts/create/
    path("create/", CreatePostView.as_view()),
    # v1/posts/explore/
    path("feed/explore/", ExplorePostView.as_view()),
    # v1/posts/feed/<str:ticker_id>/
    path("feed/<str:ticker_id>/", TickerPostFeedView.as_view()),
    # v1/posts/users/<social_user_id>/
    path("users/<str:social_user_id>/", UserPostsView.as_view()),
    # v1/posts/<post_url>/
    path("<str:post_url>/", PostURLView.as_view()),
    # v1/posts/<post_id>/remove/
    path("<str:post_id>/remove/", DeletePostView.as_view()),
    # v1/posts/<post_id>/react/
    path("<str:post_id>/react/", ReactPostView.as_view()),
    # v1/posts/<post_id>/reactions/
    path("<str:post_id>/reactions/", PostReactionsView.as_view()),
    # v1/posts/<post_id>/comments/
    path("<str:post_id>/comments/", CommentFeedView.as_view()),
    # v1/posts/<post_id>/comments/create/
    path("<str:post_id>/comments/create/", CommentPostView.as_view()),
    # v1/posts/<post_id>/comments/<comment_id>/remove/
    path(
        "<str:post_id>/comments/<str:comment_id>/remove/", DeleteCommentView.as_view()
    ),
    # v1/posts/<post_id>/comments/<comment_id>/react/
    path("<str:post_id>/comments/<str:comment_id>/react/", ReactCommentView.as_view()),
    # v1/posts/<post_id>/comments/<comment_id>/reactions/
    path(
        "<str:post_id>/comments/<str:comment_id>/reactions/",
        CommentReactionsView.as_view(),
    ),
]
