import boto3
from botocore import exceptions

from .exceptions import (
    S3BucketException, S3BucketNotFoundException, S3BucketForbiddenException)
from .credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


class AWS:
    AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
    REGION = 'us-east-1'
    SERVICE_NAME = None

    def __init__(
            self,
            aws_access_key_id: str = None,
            aws_secret_access_key: str = None,
            region: str = None) -> None:
        self.aws_access_key_id = \
            aws_access_key_id or self.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = \
            aws_secret_access_key or self.AWS_SECRET_ACCESS_KEY
        self.region = region or self.REGION
        self.session = self._get_session()
        self.client = self._get_client()

    def _get_session(self):
        session_config = {
            'aws_access_key_id': self.aws_access_key_id,
            'aws_secret_access_key': self.aws_secret_access_key,
            'region_name': self.region
        }
        return boto3.Session(**session_config)

    def _get_client(self):
        client_config = {
            'use_ssl': True,
        }
        return self.session.client(self.SERVICE_NAME, **client_config)


class S3(AWS):
    SERVICE_NAME = 's3'

    def __init__(self, bucket, *args, **kwargs):
        super(S3, self).__init__(*args, **kwargs)
        self.bucket = bucket
        self._bucket_exists()

    def _bucket_exists(self) -> None:
        """
        Determine if a bucket exists and permissions are granted to access it.
        """
        try:
            self.client.head_bucket(self.bucket)
        except exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '403':
                raise S3BucketForbiddenException(
                    'Permissions are not granted '
                    'to access bucket \"{}\".'.format(self.bucket))
            elif error_code == '404':
                raise S3BucketNotFoundException(
                    'Bucket \"{}\" does not exist.'.format(self.bucket))
            else:
                raise S3BucketException(
                    'An error occurred when accessing '
                    'bucket \"{}\".'.format(self.bucket))

    def upload_file(self, filename, key, **kwargs) -> None:
        """Upload a file."""
        self.client.upload_file(
            filename, self.bucket, key, ExtraArgs=kwargs)

    def get_object(self, key) -> None:
        """Get an object."""
        self.client.get_object(Bucket=self.bucket, Key=key)


class Transcribe(AWS):
    SERVICE_NAME = 'transcribe'

    def __init__(self, *args, **kwargs):
        super(Transcribe, self).__init__(*args, **kwargs)

    def start_transcription_job(self):
        """Start a transcription job."""
        pass
