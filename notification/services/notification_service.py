from rest_framework.exceptions import ValidationError

from common import SocketNotificationService
from notification.constants import NotificationIntent
from notification.repositories import NotificationRepository
from notification.models import Notification
from stocksmart.celery import app


class NotificationService:
    notification_repo = NotificationRepository()

    @staticmethod
    def __get_user_queryset(user_id, many=False):
        from user.services import UserService

        if many:
            return UserService().get_users_by_ids(user_id)
        return UserService().get_user_by_id(user_id)

    @staticmethod
    def __get_user_data(user, many=False):
        from user.serializers import UserNotificationSerializer

        if many:
            return UserNotificationSerializer(user, many=many).data
        return UserNotificationSerializer(user, many=many).data

    @staticmethod
    def __get_user_follower_ids(user_id):
        from user.services import UserFriendshipService

        return (
            UserFriendshipService()
            .get_user_followers_list(user_id)
            .values_list("relating_user_id", flat=True)
        )

    @staticmethod
    @app.task()
    def send_like_notification(content_id, reacted_by_user_id, content_type):
        from post.services import CommentService, PostService
        from post.serializers import (
            CommentNotificationSerializer,
            PostNotificationSerializer,
        )
        from post.constants.reactable_content import ReactableContent

        if content_type == ReactableContent.POST.value:
            content_obj = PostService().get_post_by_id_or_none(content_id)
            content_data = PostNotificationSerializer(content_obj).data
            notification_intent = NotificationIntent.LIKE_POST.value
        else:
            content_obj = CommentService().get_comment_by_id(content_id)
            post_obj = PostService().get_post_by_id_or_none(
                content_obj.content_object.id
            )
            content_data = {
                "comment": CommentNotificationSerializer(content_obj).data,
                "post": PostNotificationSerializer(post_obj).data,
            }
            notification_intent = NotificationIntent.LIKE_COMMENT.value

        reacted_by_user = NotificationService.__get_user_data(
            NotificationService.__get_user_queryset(reacted_by_user_id)
        )
        notification_payload = {
            "sender": reacted_by_user,
            "data": content_data,
            "event": notification_intent,
        }
        SocketNotificationService().send_notification(
            content_obj.created_by_user_id, notification_payload
        )
        notification_payload["sender"] = str(reacted_by_user_id)
        notification_payload["receiver"] = str(content_obj.created_by_user_id)
        NotificationService.create_notification(notification_payload)

    @staticmethod
    @app.task()
    def send_post_target_notification(post_ids):
        from post.services import PostService
        from post.serializers import PostTargetNotificationSerializer

        posts_dict = PostTargetNotificationSerializer(
            PostService().get_posts_by_ids(post_ids), many=True
        ).data
        for post in posts_dict:
            post_creator = str(post.pop("created_by_user_id"))
            notification_intent = (
                NotificationIntent.POST_TARGET_HIT.value
                if post["is_target_reached"]
                else NotificationIntent.POST_TARGET_MISS.value
            )
            notification_payload = {
                "data": post,
                "event": notification_intent,
            }
            SocketNotificationService().send_notification(
                post_creator, notification_payload
            )
            notification_payload["receiver"] = post_creator
            NotificationService.create_notification(notification_payload)

    @staticmethod
    @app.task()
    def send_comment_on_post_notification(
        notify_user_id, commented_by_user_id, comment_id
    ):
        from post.services import CommentService
        from post.serializers import (
            CommentNotificationSerializer,
            PostNotificationSerializer,
        )

        comment = CommentService().get_comment_by_id(comment_id)
        if not comment:
            return
        reacted_by_user = NotificationService.__get_user_data(comment.created_by_user)
        notification_payload = {
            "sender": reacted_by_user,
            "data": {
                "comment": CommentNotificationSerializer(comment).data,
                "post": PostNotificationSerializer(comment.content_object).data,
            },
            "event": NotificationIntent.COMMENT_ON_POST.value,
        }
        SocketNotificationService().send_notification(
            notify_user_id, notification_payload
        )
        notification_payload["sender"] = str(comment.created_by_user_id)
        notification_payload["receiver"] = str(notify_user_id)
        NotificationService.create_notification(notification_payload)

    @staticmethod
    @app.task()
    def user_follow_notification(notify_user_id, followed_by_user_id):
        from user.services import UserFriendshipService
        from user.models import UserFriendship

        friendship = UserFriendshipService().get_user_friendship_or_none(
            followed_by_user_id, notify_user_id
        )

        # Checks if the User is still being followed or not
        # During notification processing
        if (
            not friendship
            or friendship.friendship != UserFriendship.UserFriendshipType.FOLLOW
        ):
            return
        follower_user = NotificationService.__get_user_data(friendship.relating_user)
        NotificationService.create_notification(
            {
                "receiver": notify_user_id,
                "sender": friendship.relating_user_id,
                "event": NotificationIntent.FOLLOW_USER,
            }
        )
        SocketNotificationService().send_notification(
            notify_user_id,
            {
                "sender": follower_user,
                "event": NotificationIntent.FOLLOW_USER.value,
            },
        )

    @staticmethod
    @app.task()
    def send_post_created_notification(post_id):
        from post.serializers import PostNotificationSerializer
        from post.services import PostService

        post = PostService().get_post_by_id_or_none(post_id)

        # When post is deleted
        if not post:
            return

        follower_user_ids = NotificationService.__get_user_follower_ids(
            post.created_by_user_id
        )
        # When no followers present for the User
        if not follower_user_ids:
            return
        post_data = PostNotificationSerializer(post).data
        post_creator = NotificationService.__get_user_data(post.created_by_user)
        notify_service = SocketNotificationService()

        post_mentioned_user_ids = post.user_mentions.values_list("id", flat=True)
        if post_mentioned_user_ids:
            # Removes users who were mentioned in the Post
            # If they exist in the Post created user's follower list
            follower_user_ids = list(
                set(follower_user_ids) - set(post_mentioned_user_ids)
            )
            post_mention_data = {
                "sender": post_creator,
                "data": post_data,
                "event": NotificationIntent.MENTION_ON_POST.value,
            }
            for mentioned_user_id in post_mentioned_user_ids:
                notify_service.send_notification(mentioned_user_id, post_mention_data)
                NotificationService.create_notification(
                    {
                        "receiver": mentioned_user_id,
                        "sender": str(post.created_by_user_id),
                        "event": NotificationIntent.MENTION_ON_POST.value,
                        "data": post_data,
                    }
                )
        new_post_notification_data = {
            "sender": post_creator,
            "data": post_data,
            "event": NotificationIntent.NEW_POST.value,
        }
        for follower_user_id in follower_user_ids:
            notify_service.send_notification(
                follower_user_id, new_post_notification_data
            )
            NotificationService.create_notification(
                {
                    "receiver": str(follower_user_id),
                    "sender": str(post.created_by_user_id),
                    "event": NotificationIntent.NEW_POST.value,
                    "data": post_data,
                }
            )

    @staticmethod
    @app.task()
    def send_user_success_rate_notification(
        user_id, prev_success_rate, new_success_rate
    ):
        notification_payload = {
            "data": {
                "prev_success_rate": prev_success_rate,
                "new_success_rate": new_success_rate,
            },
            "event": NotificationIntent.USER_SUCCESS_RATE_CHANGE.value,
        }
        SocketNotificationService().send_notification(
            user_id,
            notification_payload,
        )
        notification_payload["receiver"] = str(user_id)
        NotificationService.create_notification(notification_payload)

    @staticmethod
    @app.task()
    def send_user_karma_notification(user_id, prev_karma, new_karma):
        notification_payload = {
            "data": {
                "prev_karma": prev_karma,
                "new_karma": new_karma,
            },
            "event": NotificationIntent.USER_KARMA_CHANGE.value,
        }
        SocketNotificationService().send_notification(
            user_id,
            notification_payload,
        )
        notification_payload["receiver"] = str(user_id)
        NotificationService.create_notification(notification_payload)

    @staticmethod
    def leaderboard_winner_notification(leaderboard_obj):
        from post.serializers import LeaderboardNotificationSerializer

        leaderboard_data = LeaderboardNotificationSerializer(leaderboard_obj).data
        notification_payload = {
            "data": {**leaderboard_data},
            "event": NotificationIntent.USER_LEADERBOARD.value,
        }
        SocketNotificationService().send_notification(
            leaderboard_obj.user_id, notification_payload
        )
        notification_payload["receiver"] = str(leaderboard_obj.user_id)
        NotificationService.create_notification(notification_payload)

    @staticmethod
    def leaderboard_results_notification(user_ids):
        notification_payload = {
            "event": NotificationIntent.LEADERBOARD_RESULTS.value,
        }
        notification_objs = []
        for user_id in user_ids:
            user_id = str(user_id)
            SocketNotificationService().send_notification(user_id, notification_payload)
            notification_objs.append(
                Notification(
                    **{
                        "receiver_id": user_id,
                        "event": NotificationIntent.LEADERBOARD_RESULTS.value,
                    }
                )
            )
        NotificationService().bulk_create_notifications(notification_objs)

    def get_user_notifications(self, user):
        return self.notification_repo.get_user_notifications(user)

    def mark_user_notifications_read(self, user):
        return self.notification_repo.mark_user_notifications_read(user)

    def get_notification_by_id(self, notification_id):
        return self.notification_repo.get_notification_by_id(notification_id)

    def mark_notification_read(self, notification_id, user_id):
        notification = self.get_notification_by_id(notification_id)
        # If a notification exists
        # and hasn't been marked as read
        # and matches the creator
        # We will mark the notification as read
        if (
            notification
            and not notification.read_at
            and str(notification.receiver_id) == user_id
        ):
            return self.notification_repo.mark_notification_read(notification)
        return False

    def get_recent_read_notification_time(self, user):
        notification = self.notification_repo.get_recent_read_notification(user)
        if notification:
            return notification.read_at
        return notification

    @staticmethod
    def create_notification(notification_data):
        from notification.serializers.notification_serializer import (
            CreateNotificationSerializer,
        )

        serializer = CreateNotificationSerializer(data=notification_data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        serializer = serializer.save()
        return serializer

    def bulk_create_notifications(self, notifications):
        return self.notification_repo.bulk_create_notifications(notifications)

    def get_unread_notifications_count(self, user):
        return self.notification_repo.get_unread_notifications_count(user)
