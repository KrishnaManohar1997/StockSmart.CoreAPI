from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = "uploads"
    default_acl = "public-read"
    file_overwrite = False
