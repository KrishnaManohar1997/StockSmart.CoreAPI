from common.base_view import BaseView
from post.services import ReactionService


class ReactCommentView(BaseView):
    reaction_service = ReactionService()

    def post(self, request, post_id, comment_id):
        requested_reaction = request.data.get("reaction")
        if not requested_reaction:
            return self.bad_request_response("Invalid request")
        is_reacted, message = self.reaction_service.react_on_comment(
            request.user.id, post_id, comment_id, requested_reaction
        )
        if not is_reacted:
            return self.bad_request_response(message=message)
        return self.success_response(message=message)
