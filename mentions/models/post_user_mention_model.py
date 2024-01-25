from django.db import models

from common.models import BaseModel
from post.models import Post
from user.models import User


class PostUserMention(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    mentioned_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Post_User_Mention"
        verbose_name_plural = "Post User Mentions"
        db_table = "Post_User_Mention"
