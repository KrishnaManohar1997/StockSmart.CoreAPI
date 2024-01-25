# Sizes depicted in Bytes
MAXIMUM_SUPPORTED_SIZE = {
    # 1 MB
    "image": 1048576,
    # Currently the following Media is Unsupported
    "audio": 16777216,
    "document": 104857600,
    "application": 104857600,
    "sticker": 102400,
    "video": 16777216,
}

UNSUPPORTED_MEDIA_MSG = (
    "Unsupported media, Please try uploading an Image (jpeg/jpg/png)."
)
MEDIA_VALIDATION_LARGE_FILE_MSG = (
    "Please try uploading an {media_type} file of size <= {file_size_mb} MB."
)
