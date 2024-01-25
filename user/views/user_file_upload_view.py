from common.base_view import BaseView
from common.constants import FileUploadContext
from common.helper import FileUploader
from common.media_validation_util import MediaValidationService


class UserFileUploadView(BaseView):
    def post(self, request):
        file_object = request.FILES.get("file")
        if not file_object:
            return self.bad_request_response("Invalid request")

        upload_context = request.data.get(
            "upload_context", FileUploadContext.default_context()
        )
        if not FileUploadContext.has_value(upload_context):
            return self.bad_request_response("Invalid Context")

        # Validations for Filesize and type
        is_valid, message = MediaValidationService.validate_media_content(file_object)
        if not is_valid:
            return self.bad_request_response(message)

        file_url = FileUploader().get_file_url(request, file_object, upload_context)
        return self.data_response("Uploaded", {"file_url": file_url})
