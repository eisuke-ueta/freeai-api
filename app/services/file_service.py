import os
import secrets

from PIL import Image
from werkzeug.datastructures import FileStorage

from app.aws.s3_client import S3Client
from app.commons.context import Context


class FileService(object):

    DEFAULT_DIR = "default"

    FILE_TYPE_JPEG = "jpeg"

    MIME_TYPE_PNG = "image/png"
    MIME_TYPE_JPEG = "image/jpeg"

    def __init__(self, context: Context) -> None:
        self.context = context
        self.logger = context.logger
        self.config = context.config

    def upload(self, fileStorageObj: FileStorage) -> list:
        # Save original file to tmp directory
        filename = self._generate_filename(fileStorageObj.filename)
        file_path = os.path.join(self.config.TMP_DIR, filename)
        fileStorageObj.save(file_path)

        # Convert to jpeg
        mimetype = fileStorageObj.mimetype
        if mimetype == self.MIME_TYPE_PNG:
            file_path = self._convert_from_png(file_path)

        # Upload to S3
        basename = os.path.basename(file_path)
        key = os.path.join(self.DEFAULT_DIR, basename)
        object_url = S3Client(self.context).upload_file(
            file_path, key, is_public=True, content_type=self.MIME_TYPE_JPEG)

        return [object_url]

    def delete(self, id: str) -> str:
        return ""

    @staticmethod
    def _generate_filename(filename: str) -> str:
        extention = os.path.splitext(filename)[1]
        basename = secrets.token_urlsafe(16)
        return basename + extention

    def _convert_from_png(self, file_path: str) -> str:
        # Convert to png
        image = Image.open(file_path)
        rgb_image = image.convert('RGB')

        # Generate file path
        filename = os.path.basename(file_path)
        basename = os.path.splitext(filename)[0]
        new_filename = basename + "." + self.FILE_TYPE_JPEG
        new_file_path = os.path.join(self.config.TMP_DIR, new_filename)

        # Save image
        rgb_image.save(new_file_path)

        # Delete original file
        os.remove(file_path)

        return new_file_path
