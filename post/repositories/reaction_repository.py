from post.models import Reaction


class ReactionRepository:
    def get_user_reaction_to_content(self, content_id, user_id):
        return Reaction.objects.get(created_by_user_id=user_id, object_id=content_id)

    def remove_reaction(self, reaction) -> None:
        reaction.delete()

    def add_reaction_to_content(self, user_id, content_object, reaction) -> Reaction:
        return Reaction.objects.create(
            created_by_user_id=user_id, content_object=content_object, reaction=reaction
        )

    def update_reaction(self, reaction, requested_reaction):
        reaction.reaction = requested_reaction
        reaction.save()
        return reaction

    def get_content_reacted_by_user(self, object_ids: list, requested_user_id: str):
        return Reaction.objects.filter(
            object_id__in=object_ids, created_by_user_id=requested_user_id
        )

    def get_content_reactions(self, content_id, blocked_by_users):
        return (
            Reaction.objects.filter(object_id=content_id, reaction="Like")
            .exclude(created_by_user_id__in=blocked_by_users)
            .order_by("-created_at")
            .prefetch_related("created_by_user")
        )
