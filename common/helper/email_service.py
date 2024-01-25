from django.conf import settings
from django.core.mail import EmailMessage
from stocksmart.celery import app


class EmailService:
    @staticmethod
    @app.task
    def send_email(
        from_email_address: str,
        to_email_addresses: list,
        subject: str,
        body: str,
        cc_email_addresses: list = [],
        bcc_email_addresses: list = [],
    ):
        """
        Sends an email with attachment
        Args are self explanatory
            from_email_address: str
            to_email_addresses: list
            subject: str
            body: str > Text content of the body
            cc_email_addresses: list = [],
            bcc_email_addresses: list = [],
            attachment_files: List[AttachmentFile]: List of attachment files
        """
        if settings.APP_ENVIRONMENT != "PRODUCTION":
            subject = f"{subject} - [{settings.APP_ENVIRONMENT}]"

        msg = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email_address,
            to=to_email_addresses,
            bcc=bcc_email_addresses,
            cc=cc_email_addresses,
        )
        msg.make_private = True
        msg.send(fail_silently=False)

    @staticmethod
    @app.task
    def send_template(
        from_email_address: str,
        to_email_addresses: list,
        template_id: str,
        cc_email_addresses: list = [],
        bcc_email_addresses: list = [],
        merge_variables: dict = {},
    ):
        msg = EmailMessage(
            from_email=from_email_address,
            to=to_email_addresses,
            bcc=bcc_email_addresses,
            cc=cc_email_addresses,
        )
        msg.template_id = template_id
        msg.dynamic_template_data = merge_variables
        msg.make_private = True
        msg.send(fail_silently=False)


class EmailTemplate:
    SIGNUP_WELCOME_EMAIL = "d-95563c8e9acb4b7fb9851f35e3a67682"
    LEADERBOARD_WINNER_EMAIL = "d-94aeca9c207c48859e6633265cb76686"
    LEADERBOARD_RESULTS_EMAIL = "d-8cd0f63b11a64f4e9d3dd5c982b811c4"
