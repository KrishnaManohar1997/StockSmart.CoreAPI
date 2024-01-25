from common.constants.base_enum import BaseEnum


class FileUploadContext(BaseEnum):

    MEDIA = "media"
    PROFILE = "profile"

    @staticmethod
    def default_context():
        return FileUploadContext.MEDIA
