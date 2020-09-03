import os
import logging
from pathlib import Path

import boto3

_logger = logging.getLogger(__name__)


class Bucket:

    def __init__(self) -> None:
        super().__init__()

        self._aws_s3_bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")
        self._aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self._aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

        self._aws_s3_bucket_model_folder = os.environ.get("ENVIRONMENT")

        session = boto3.Session(
            aws_access_key_id=self._aws_access_key_id,
            aws_secret_access_key=self._aws_secret_access_key,
        )
        s3 = session.resource('s3')

        self.aws_s3_bucket = s3.Bucket(self._aws_s3_bucket_name)

    def upload_file(self, file_path: Path):
        _logger.info(f"Uploading {file_path} to AWS S3")

        self.aws_s3_bucket.upload_file(str(file_path), f"{self._aws_s3_bucket_model_folder}/{file_path.name}")

        _logger.info(f"{file_path} successfully uploaded")

    def download_file(self):
        pass

    def get_last_model(self):
        pass


bucket = Bucket()
bucket.upload_file(Path("1597941820.118.pkl"))
