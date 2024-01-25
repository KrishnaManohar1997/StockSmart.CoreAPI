from rest_framework.pagination import LimitOffsetPagination

from common.base_view import PublicBaseView
from common.helper.get_limited_paginated_results import get_limited_paginated_results
from post.serializers import CommentsViewSerializer
from post.services import CommentService, ReactionService


class CommentFeedView(PublicBaseView):
    comment_service = CommentService()
    reaction_service = ReactionService()

    def __merge_comments_user_reaction(
        self, paginated_comments_data, requested_user_id
    ):
        comment_ids = []
        comments_data_dict = []
        for comment in paginated_comments_data:
            comment_dict = dict(dict(comment))
            comments_data_dict.append(comment_dict)
            comment_ids.append(comment_dict["id"])
        reacted_comments_list = self.reaction_service.get_content_reacted_by_user(
            comment_ids, requested_user_id
        ).values_list("object_id", flat=True)
        reacted_comments = [str(comment_id) for comment_id in reacted_comments_list]
        return {
            "comments": comments_data_dict,
            "reacted_by_user": reacted_comments,
        }

    def get(self, request, post_id):

        paginator = LimitOffsetPagination()
        comments_queryset = self.comment_service.get_post_comments(
            post_id, request.user.id
        )
        if not comments_queryset:
            return self.empty_paginated_response(message="Comments on post")
        if request.user.is_authenticated:
            paginated_comments_queryset = paginator.paginate_queryset(
                comments_queryset, request
            )
        else:
            paginated_comments_queryset = get_limited_paginated_results(
                request, comments_queryset, paginator, 3
            )
        comments_data = CommentsViewSerializer(
            paginated_comments_queryset, many=True
        ).data
        comments_json = self.__merge_comments_user_reaction(
            comments_data, request.user.id
        )
        return self.paginated_response(paginator, "Comments", comments_json)
