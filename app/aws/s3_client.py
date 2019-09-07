import json
from typing import Any

import boto3
from botocore.exceptions import ClientError

from app.commons.context import Context


class S3Client(object):

    BASE_S3_URL = 'https://{}.s3.amazonaws.com/{}'

    def __init__(self, context: Context):
        self.s3 = boto3.client('s3')
        self.logger = context.logger
        self.bucket = context.config.AWS_S3_BUCKET

    def get_object(self, key: str) -> Any:
        response = self.s3.get_object(Bucket=self.bucket, Key=key)
        body = response['Body'].read().decode('utf-8')
        return json.loads(body)

    def put_object(self, key: str, content: Any) -> str:
        self.s3.put_object(Bucket=self.bucket,
                           Key=key,
                           Body=json.dumps(content, ensure_ascii=False),
                           ContentType='application/json')
        return key

    def upload_file(self, filename: str, key: str, is_public: bool = False, content_type: str = None) -> str:
        """
        Upload a file to an S3 bucket.

        :param file_name: File to upload
        :param key: S3 object key.
        :return: S3 Object URL
        """

        self.logger.info('filename: {}, key:{}'.format(filename, key))

        
        extra_args = {}
        if is_public:
            extra_args['ACL'] = 'public-read'
        if content_type:
            extra_args['ContentType'] = content_type

        try:
            self.s3.upload_file(Filename=filename, Bucket=self.bucket, Key=key, ExtraArgs=extra_args)
            return self.BASE_S3_URL.format(self.bucket, key)
        except ClientError as e:
            self.logger.error(e)
            return None
