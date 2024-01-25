import os

from common.helper.generate_random_filename import get_random_file_name
from common.media_validation_util import MediaValidationService
from stocksmart.storage_backends import PublicMediaStorage


class FileUploader:
    media_storage = PublicMediaStorage()

    def get_file_url(self, request, file_object, upload_context) -> str:

        # organize a path for the file in bucket
        file_directory_within_bucket = f"{request.user.id}/{upload_context}/"
        file_extension = MediaValidationService.get_file_extension(file_object.name)
        file_name = f"{get_random_file_name()}.{file_extension}"

        # synthesize a full file path; note that we included the filename
        file_path_within_bucket = os.path.join(file_directory_within_bucket, file_name)
        self.media_storage.save(file_path_within_bucket, file_object)

        return self.media_storage.url(file_path_within_bucket)
