from rest_framework.permissions import IsAuthenticated

from common.base_view import BaseView
from report.services import ReportService
from user.permissions import IsBlockedByUser


class ReportUserView(BaseView):
    permission_classes = [IsAuthenticated, IsBlockedByUser]
    report_service = ReportService()

    def post(self, request, social_user_id: str):
        # You cannot report yourself
        if social_user_id == str(request.user.id):
            return self.bad_request_response("Invalid Request")
        report, message = self.report_service.report_user(request.user, social_user_id)
        if not report:
            return self.bad_request_response(message=message)
        return self.resource_created_response(resource="Report", resource_id=report.id)
