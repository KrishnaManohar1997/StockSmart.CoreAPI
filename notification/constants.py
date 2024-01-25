from django.db import models


class NotificationIntent(models.TextChoices):
    LIKE_POST = "LikePost"
    LIKE_COMMENT = "LikeComment"
    NEW_POST = "NewPost"
    COMMENT_ON_POST = "CommentOnPost"
    MENTION_ON_POST = "MentionOnPost"
    FOLLOW_USER = "FollowUser"
    USER_SUCCESS_RATE_CHANGE = "UserSuccessRateChange"
    USER_KARMA_CHANGE = "UserKarmaChange"
    USER_LEADERBOARD = "UserLeaderboard"
    LEADERBOARD_RESULTS = "LeaderboardResults"
    POST_TARGET_HIT = "PostTargetHit"
    POST_TARGET_MISS = "PostTargetMiss"
