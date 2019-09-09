import pytesseract
from PIL import Image

from app.aws.s3_client import S3Client
from app.commons.context import Context


class OcrService(object):

    TESSERACT_LANG = 'jpn'
    TESSERACT_CONFIG = '--psm 6'

    def __init__(self, context: Context) -> None:
        self.context = context
        self.logger = context.logger
        self.config = context.config

    def execute(self, image_url: str) -> str:
        # Download file
        filename = S3Client(self.context).download_file(
            image_url, self.config.TMP_DIR)

        # OCR
        raw_text = pytesseract.image_to_string(Image.open(filename),
                                               lang=self.TESSERACT_LANG,
                                               config=self.TESSERACT_CONFIG)

        # Post process

        return raw_text
