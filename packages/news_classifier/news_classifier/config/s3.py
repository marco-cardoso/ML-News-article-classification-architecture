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

    def download_file(self, filename: str):
        _logger.info(f"Downloading {filename} from AWS S3")

        self.aws_s3_bucket.download_file(f"{self._aws_s3_bucket_model_folder}/{filename}", filename)

        _logger.info(f"{filename} successfully downloaded")

    def get_environment_objects_mask(self, object) -> bool:
        """
        Return if the given object is from the current environment folder or not
        :param object: An AWS S3 object
        :return: A boolean representing whether the object is from the current environment folder or not
        """
        is_object = (object.size > 0)
        is_in_environment_folder = (object.key.split("/")[0] == self._aws_s3_bucket_model_folder)
        return is_object and is_in_environment_folder

    def get_last_model_name(self):
        # Get bucket objects
        objects = list(self.aws_s3_bucket.objects.all())
        # Get objects inside the environment folder and with size > 0
        objects = list(filter(self.get_environment_objects_mask, objects))
        # Get the last uploaded model
        objects = sorted(objects, key=lambda obj: obj.last_modified, reverse=True)
        latest_model_meta_data = objects[0]
        model_name = Path(latest_model_meta_data.key).stem
        return model_name



