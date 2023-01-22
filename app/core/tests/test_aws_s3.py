"""AWS Mock"""
from django.test import TestCase

import boto3

from tempfile import NamedTemporaryFile, gettempdir

from moto import mock_s3


BUCKET_NAME = "mybucket"


def create_bucket():
    s3 = boto3.resource("s3")
    bucket = s3.create_bucket(Bucket=BUCKET_NAME)
    return s3, bucket


def verify_upload(filename):
    client = boto3.client("s3")
    resp = client.get_object(Bucket=BUCKET_NAME, Key=filename)
    return resp['ResponseMetadata']['HTTPHeaders']['content-length']


def test_upload(bucket):
    with NamedTemporaryFile() as tmp:
        tmp.write(b'Hi dear')
        tmp.flush()
        filename = tmp.name.replace(gettempdir() + '/', '')
        bucket.upload_file(tmp.name, filename)
        return filename


class MockAWSTests(TestCase):

    @mock_s3
    def test_bucket_resource(self):
        _, bucket = create_bucket()
        filename = test_upload(bucket)
        content_length = verify_upload(filename)
        self.assertGreater(int(content_length), 0)
