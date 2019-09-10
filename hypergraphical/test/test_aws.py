from unittest.mock import Mock
from botocore import exceptions

from .base import AWSBaseTestCase
from ..aws import S3, Transcribe
from ..exceptions import (
    S3BucketException, S3BucketNotFoundException, S3BucketForbiddenException)


class AWSTestCase(AWSBaseTestCase):
    def setUp(self):
        super(AWSTestCase, self).setUp()

    def test_get_session(self):
        self.aws._get_session()
        self.mock_session.assert_called_with(
                aws_access_key_id='aws_access_key_id',
                aws_secret_access_key='aws_secret_access_key',
                region_name='region'
        )

    def test_get_client(self):
        self.aws._get_client()
        self.session.client.assert_called_with(None, use_ssl=True)


class S3TestCase(AWSBaseTestCase):
    def setUp(self):
        super(S3TestCase, self).setUp()
        self.bucket = 'bucket'
        self.s3 = S3(self.bucket)
        self.s3.client = Mock()

    def test_bucket_exists(self):
        self.assertIsNone(self.s3._bucket_exists())

    def test_bucket_exists_forbidden(self):
        self.s3.client.head_bucket.side_effect = \
            exceptions.ClientError({'Error': {'Code': '403'}}, 'HeadBucket')
        with self.assertRaises(S3BucketForbiddenException) as context:
            self.s3._bucket_exists()
        self.assertEqual(
            'Permissions are not granted to access bucket \"bucket\".',
            str(context.exception))

    def test_bucket_exists_not_found(self):
        self.s3.client.head_bucket.side_effect = \
            exceptions.ClientError({'Error': {'Code': '404'}}, 'HeadBucket')
        with self.assertRaises(S3BucketNotFoundException) as context:
            self.s3._bucket_exists()
        self.assertEqual(
            'Bucket \"bucket\" does not exist.', str(context.exception))

    def test_bucket_exists_exception(self):
        self.s3.client.head_bucket.side_effect = \
            exceptions.ClientError({'Error': {'Code': ''}}, '')
        with self.assertRaises(S3BucketException) as context:
            self.s3._bucket_exists()
        self.assertEqual(
            'An error occurred when accessing bucket \"bucket\".',
            str(context.exception))

    def test_upload_file(self):
        extra_args = {'a': 1, 'b': 2, 'c': 3}
        self.s3.upload_file('filename', 'key', **extra_args)
        self.s3.client.upload_file.assert_called_with(
            'filename', 'bucket', 'key', ExtraArgs=extra_args
        )

    def test_get_object(self):
        self.s3.get_object('key')
        self.s3.client.get_object.assert_called_with(
            Bucket=self.bucket, Key='key')


class TranscribeTestCase(AWSBaseTestCase):
    def setUp(self):
        super(TranscribeTestCase, self).setUp()
        self.transcribe = Transcribe()
        self.transcribe.client = Mock()

    def test_start_transcription_job(self):
        self.assertIsNone(self.transcribe.start_transcription_job())
