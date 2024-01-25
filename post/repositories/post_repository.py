import structlog
from django.db import transaction
from django.db.models import F

from post.models import Post

logger = structlog.getLogger("django.server")


class PostRepository:
    def get_posts_excluded_by_blocked_users(self, blocked_user_id_list: list = None):
        return Post.objects.exclude(
            created_by_user_id__in=blocked_user_id_list
        ).prefetch_related("created_by_user")

    def get_recent_post_feed(self, blocked_user_id_list: list = None):
        return self.get_posts_excluded_by_blocked_users(blocked_user_id_list).order_by(
            "-created_at"
        )

    def get_popular_post_feed(self, blocked_user_id_list: list = None):
        return self.get_posts_excluded_by_blocked_users(blocked_user_id_list).order_by(
            "-reaction_count"
        )

    def get_most_engaged_post_feed(self, blocked_user_id_list: list = None):
        return self.get_posts_excluded_by_blocked_users(blocked_user_id_list).order_by(
            "-comment_count"
        )

    def get_target_post_feed(self, blocked_user_id_list: list = None):
        return (
            self.get_posts_excluded_by_blocked_users(blocked_user_id_list)
            .filter(target_price__isnull=False)
            .order_by("-created_at")
        )

    def get_verified_post_feed(self, blocked_user_id_list: list = None):
        return (
            self.get_posts_excluded_by_blocked_users(blocked_user_id_list)
            .filter(created_by_user__verified_professional_accounts__isnull=False)
            .order_by("-created_at")
        )

    def get_stock_post_feed(self, blocked_user_id_list: list = None):
        return (
            self.get_posts_excluded_by_blocked_users(blocked_user_id_list)
            .filter(source__ticker_type="Stock")
            .order_by("-created_at")
        )

    def get_smallcase_post_feed(self, blocked_user_id_list: list = None):
        return (
            self.get_posts_excluded_by_blocked_users(blocked_user_id_list)
            .filter(source__ticker_type="Smallcase")
            .order_by("-created_at")
        )

    def get_post_by_id(self, post_id):
        return Post.objects.get(id=post_id)

    def update_post_reaction_count(self, post, is_reaction_added: bool):
        if is_reaction_added:
            post.reaction_count = F("reaction_count") + 1
        else:
            post.reaction_count = F("reaction_count") - 1

        post.save(update_fields=["reaction_count"])

    def update_comment_count(self, post, is_comment_added: bool = True):
        if is_comment_added:
            post.comment_count = F("comment_count") + 1
        else:
            post.comment_count = F("comment_count") - 1

        post.save(update_fields=["comment_count"])

    # Currently Unused
    def get_ticker_post_feed(self, ticker_id: str, blocked_user_ids: list):
        return (
            Post.objects.filter(mentions__ticker_ids__contains=str(ticker_id))
            .exclude(created_by_user_id__in=blocked_user_ids)
            .prefetch_related("created_by_user")
        )

    def get_post_by_url(self, post_url: str, blocked_user_ids: str):
        return (
            Post.objects.filter(url=post_url)
            .exclude(created_by_user_id__in=blocked_user_ids)
            .prefetch_related("created_by_user")
        )

    @transaction.atomic
    def delete_post(self, post):
        from mentions.models import PostUserMention, PostTickerMention

        try:
            with transaction.atomic():
                if post.user_mentions:
                    PostUserMention.objects.filter(post=post).delete()
                post.ticker_mentions.all().delete()

                post.comments.all().delete()
                post.reactions.all().delete()
                post.delete()
            return True
        except Exception as error:
            logger.error(f"Failed deleting post {post.id} {error}")
        return False

    def get_posts_by_ids(self, post_ids):
        return Post.objects.filter(id__in=post_ids)
