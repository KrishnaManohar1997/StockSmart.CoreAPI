import imghdr
import pathlib
from typing import Tuple

from common.media_validation_util.constants import (
    MAXIMUM_SUPPORTED_SIZE,
    MEDIA_VALIDATION_LARGE_FILE_MSG,
    UNSUPPORTED_MEDIA_MSG,
)
from common.mime_type_constants import MEDIA_CONTENT_TYPE_MAPPING


class MediaValidationService:
    @staticmethod
    def get_file_extension(file_name: str) -> str:
        return pathlib.Path(file_name).suffix.strip(".").lower()

    @staticmethod
    def validate_media_content(file) -> Tuple[bool, str]:
        file_extension = MediaValidationService.get_file_extension(file.name)
        # File type validation
        if file_extension not in MEDIA_CONTENT_TYPE_MAPPING.keys():
            return (False, UNSUPPORTED_MEDIA_MSG)

        # Content Validation if the actual file is image or not
        if imghdr.what(file) is None:
            return (False, UNSUPPORTED_MEDIA_MSG)
        # Size validation
        media_type = MEDIA_CONTENT_TYPE_MAPPING.get(file_extension)["type"]
        max_supported_size = MAXIMUM_SUPPORTED_SIZE.get(media_type)
        if file.size > max_supported_size:
            return (
                False,
                MEDIA_VALIDATION_LARGE_FILE_MSG.format(
                    media_type=media_type,
                    file_size_mb=round(
                        MAXIMUM_SUPPORTED_SIZE.get(media_type) / (1024 * 1024), 5
                    ),
                ),
            )

        return True, ""
