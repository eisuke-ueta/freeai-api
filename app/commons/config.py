import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):

    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')
    APP_SECRET = os.getenv('APP_SECRET')

    ROOT_DIR = os.getcwd()
    TMP_DIR = os.path.join(ROOT_DIR, 'tmp')

    def __init__(self) -> None:
        os.makedirs(self.TMP_DIR, exist_ok=True)
