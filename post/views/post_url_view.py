from common.base_view import BaseView
from post.serializers import PostFeedSerializer
from post.services import PostService, ReactionService


class PostURLView(BaseView):
    post_service = PostService()
    serializer = PostFeedSerializer
    reaction_service = ReactionService()

    def get(self, request, post_url: str):
        post = self.post_service.get_post_by_url(post_url, request.user.id)
        if not post:
            return self.resource_not_found_response(resource="Post", id=post_url)
        post_data = self.serializer(post, many=True).data
        post_reaction_data = self.reaction_service.merge_posts_with_user_reaction(
            post_data, request.user.id
        )
        return self.data_response(message="Post", data=post_reaction_data)
