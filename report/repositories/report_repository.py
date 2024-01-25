from report.models import Report


class ReportRepository:
    def report_user(self, reporting_user, report_recipient_user):
        return Report.objects.create(
            created_by_user=reporting_user, content_object=report_recipient_user
        )

    def has_user_already_reported(self, reporting_user, report_recipient_user):
        return report_recipient_user.reports.filter(
            created_by_user=reporting_user
        ).exists()
