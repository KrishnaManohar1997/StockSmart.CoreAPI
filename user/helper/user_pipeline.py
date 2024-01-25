import random

import structlog
from django.conf import settings
from social_core.exceptions import AuthFailed

from common.constants import get_ss_user_ids
from common.helper import EmailService, EmailTemplate
from common.models import SignupMethod
from user.services.user_friendship_service import create_auto_follow_relation
from watchlist.models.watchlist_model import Watchlist

logger = structlog.getLogger("django.server")


def __update_profile_picture(
    user, response, profile_picture_key, is_newly_created: bool
):
    profile_picture_url = response.get(profile_picture_key, None)
    # If Newly created user and Social Profile picture is not empty
    if (is_newly_created and user) and (profile_picture_url is not None):
        user.profile_picture_url = profile_picture_url
    return user


def __update_name(user, name):
    if user.name in ["", None]:
        user.name = name
    return user


def __map_user_google_data(user, response, is_newly_created):
    # If newly created, save the Signup method
    if is_newly_created and user:
        user.signup_method = SignupMethod.GOOGLE.value
    user = __update_profile_picture(user, response, "picture", is_newly_created)
    user.save()
    return {"user": user}


def __map_user_twitter_data(user, response, is_newly_created):
    if user.email == "" or user.email == None:
        user.watchlist.delete()
        user.delete()
        raise AuthFailed(
            "Twitter",
            "Please verify/attach your twitter with an Email address to sign-in back",
        )
    # If newly created, save the Signup method
    if is_newly_created and user:
        user.signup_method = SignupMethod.TWITTER.value
    user = __update_profile_picture(
        user, response, "profile_image_url_https", is_newly_created
    )
    user.save()
    return {"user": user}


def cleanup_social_account(backend, uid, user=None, *args, **kwargs):
    """
    3rd party: python-social-auth.

    Social auth pipeline to cleanup the user's data.
    Must be placed after 'social_core.pipeline.user.create_user'.
    """
    response = kwargs["response"]
    is_newly_created_user = kwargs.get("is_new", False)
    if is_newly_created_user:
        user.is_email_verified = True
        try:
            Watchlist.objects.create(created_by_user=user)
        except Exception as error:
            logger.error(
                f"Creating Watchlist failed for User {user.username}", error=error
            )
    # Updates Name if empty
    user = __update_name(user, response.get("name"))
    user_dict = {"user": user}
    if backend.name == "twitter":
        user_dict = __map_user_twitter_data(user, response, is_newly_created_user)
    if backend.name == "google-oauth2":
        user_dict = __map_user_google_data(user, response, is_newly_created_user)
    if is_newly_created_user:
        for rand_user_id in random.sample(get_ss_user_ids(settings.APP_ENVIRONMENT), 2):
            create_auto_follow_relation.apply_async(
                args=[user.id, rand_user_id],
                countdown=random.randint(100, 300),  # 1.5 - 5 Minutes delay
            )

        email_details = {
            "name": user.name,
            "profile_url": user.profile_picture_url,
        }
        # EmailService.send_template.delay(
        #     settings.SS_FROM_EMAIL,
        #     [user.email],
        #     EmailTemplate.SIGNUP_WELCOME_EMAIL,
        #     merge_variables=email_details,
        # )

    return user_dict
