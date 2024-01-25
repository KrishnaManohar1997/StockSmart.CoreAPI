from mentions.models import PostUserMention


class UserMentionService:
    def create_post_user_mentions(self, post, users: list):
        post_id = post.id
        created_by_user_id = post.created_by_user_id
        return PostUserMention.objects.bulk_create(
            [
                PostUserMention(
                    post_id=post_id,
                    mentioned_user_id=user.id,
                    created_by_user_id=created_by_user_id,
                )
                for user in users
            ]
        )
