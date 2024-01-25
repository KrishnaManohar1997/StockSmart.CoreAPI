from user.services import UserService
from report.repositories import ReportRepository


class ReportService:
    user_service = UserService()
    report_repo = ReportRepository()

    def report_user(self, reporting_user, report_recipient_user_id: str):
        report_recipient_user = self.user_service.get_user_by_id_or_none(
            report_recipient_user_id
        )

        # If the target or report receiving user doesn't exist
        if not report_recipient_user:
            return None, "User doesn't exist"

        # When the User has already been reported
        if self.report_repo.has_user_already_reported(
            reporting_user, report_recipient_user
        ):
            return None, "User already reported"

        # Returns Report Object with Success message
        return (
            self.report_repo.report_user(reporting_user, report_recipient_user),
            "Report submitted",
        )
