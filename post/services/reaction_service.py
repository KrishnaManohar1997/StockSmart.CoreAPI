from django.core.exceptions import ValidationError

from common.helper import DateTimeHelper
from notification.services import NotificationService
from post.constants.reactable_content import ReactableContent
from post.models import Reaction
from post.repositories import ReactionRepository
from post.services import PostService
from post.services.comment_service import CommentService
from user.services import UserFriendshipService


class ReactionService:
    post_service = PostService()
    comment_service = CommentService()
    user_friendship_service = UserFriendshipService()
    reaction_repo = ReactionRepository()

    def get_user_reaction_to_content_or_none(self, content_id, user_id):
        try:
            return self.reaction_repo.get_user_reaction_to_content(content_id, user_id)
        except Reaction.DoesNotExist:
            return None

    def __add_reaction_to_content(self, user_id, post, requested_reaction):
        return self.reaction_repo.add_reaction_to_content(
            user_id, post, requested_reaction
        )

    def __update_reaction(self, reaction, requested_reaction):
        return self.reaction_repo.update_reaction(reaction, requested_reaction)

    def __validate_is_user_react_action_valid(self, post_id, reaction_by_user_id):
        post = self.post_service.get_post_by_id_or_none(post_id)
        if post is None:
            raise ValidationError("Post not found", code=404)
        self.user_friendship_service.is_requesting_user_blocked_by_user(
            requesting_user_id=reaction_by_user_id,
            target_user_id=post.created_by_user_id,
            raise_error=True,
        )
        return post

    def react_on_comment(
        self, reaction_by_user_id, post_id, comment_id, requested_reaction
    ):
        self.__validate_is_user_react_action_valid(post_id, reaction_by_user_id)
        comment = self.comment_service.get_comment_on_post_by_id_or_none(
            post_id, comment_id
        )
        if not comment:
            raise ValidationError("Invalid Comment", code=404)
        comment_reaction = self.get_user_reaction_to_content_or_none(
            comment_id, reaction_by_user_id
        )
        return self.reaction_resolver(
            ReactableContent.COMMENT,
            reaction_by_user_id,
            comment,
            requested_reaction,
            comment_reaction,
        )

    def react_on_post(self, reaction_by_user_id, post_id, requested_reaction):
        post = self.__validate_is_user_react_action_valid(post_id, reaction_by_user_id)
        post_reaction = self.get_user_reaction_to_content_or_none(
            post.id, reaction_by_user_id
        )
        return self.reaction_resolver(
            ReactableContent.POST,
            reaction_by_user_id,
            post,
            requested_reaction,
            post_reaction,
        )

    def __get_notification_delay_for_content(self, content_obj):
        MAX_DELAY_SECONDS = 300
        seconds_since_post_created = (
            DateTimeHelper.get_utc_datetime() - content_obj.created_at
        ).seconds
        if seconds_since_post_created < MAX_DELAY_SECONDS:
            return MAX_DELAY_SECONDS - seconds_since_post_created
        return 0

    def reaction_resolver(
        self,
        content_type,
        reaction_by_user_id,
        content_object,
        requested_reaction,
        reaction_obj,
    ):
        if content_type not in ReactableContent:
            return False, "Invalid Content"
        if requested_reaction not in Reaction.ReactionType:
            return False, "Invalid Reaction"
        if requested_reaction == Reaction.ReactionType.REMOVE_REACTION:
            if reaction_obj is None:
                return True, "Ok"
            # if reaction exists and requested reaction is Removing
            self.reaction_repo.remove_reaction(reaction_obj)
            if content_type == ReactableContent.POST:
                self.post_service.update_post_reaction_count(
                    content_object, is_reaction_added=False
                )
            if content_type == ReactableContent.COMMENT:
                self.comment_service.update_comment_reaction_count(
                    content_object, is_reaction_added=False
                )
            return True, "Ok"

        # If a reaction already exists
        if reaction_obj:
            # Update reaction on Post
            if reaction_obj.reaction != requested_reaction:
                self.__update_reaction(reaction_obj, requested_reaction)
                return True, "Ok"
            # If requested reaction is same as existing Reaction
            return True, "Ok"

        # Add Reaction to post/comment as object by User
        self.__add_reaction_to_content(
            reaction_by_user_id, content_object, requested_reaction
        )
        notification_countdown = 0
        if content_type == ReactableContent.POST:
            self.post_service.update_post_reaction_count(
                content_object, is_reaction_added=True
            )
            # Takes Delay on Post
            notification_countdown = self.__get_notification_delay_for_content(
                content_object
            )

        if content_type == ReactableContent.COMMENT:
            self.comment_service.update_comment_reaction_count(
                content_object, is_reaction_added=True
            )

            # Takes Delay on Post
            notification_countdown = self.__get_notification_delay_for_content(
                content_object.content_object
            )
            # Adds Delay on Comment
            notification_countdown += self.__get_notification_delay_for_content(
                content_object
            )

        if str(content_object.created_by_user_id) != str(reaction_by_user_id):
            NotificationService.send_like_notification.apply_async(
                args=[
                    str(content_object.id),
                    reaction_by_user_id,
                    content_type.value,
                ],
                countdown=0,
            )
        return True, "Ok"

    def get_content_reacted_by_user(self, object_ids: list, requested_user_id):
        return self.reaction_repo.get_content_reacted_by_user(
            object_ids, requested_user_id
        )

    def merge_posts_with_user_reaction(
        self, posts_data_dict: list, requested_user_id: str
    ):
        """Merges post data and reactions of the requesting user

        Args:
            posts_data_dict (list): List of post dictionaries
            requested_user_id (str): user requesting the content

        Returns:
            return {
                "posts": posts_data_dict,
                "reacted_by_user": reacted_posts,
            }
        """
        # Handles Anonymous user requests
        if requested_user_id is None:
            return {"posts": posts_data_dict, "reacted_by_user": []}
        post_ids = [post["id"] for post in posts_data_dict]
        reacted_posts_list = self.get_content_reacted_by_user(
            post_ids, requested_user_id
        ).values_list("object_id", flat=True)
        reacted_posts = [str(post_id) for post_id in reacted_posts_list]
        return {
            "posts": posts_data_dict,
            "reacted_by_user": reacted_posts,
        }

    def get_content_reactions(self, content_id, blocked_by_users):
        return self.reaction_repo.get_content_reactions(content_id, blocked_by_users)
