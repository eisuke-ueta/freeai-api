# from logging import DEBUG, StreamHandler, getLogger

# logger = getLogger(__name__)
# handler = StreamHandler()
# handler.setLevel(DEBUG)
# logger.setLevel(DEBUG)
# logger.addHandler(handler)

from flask import Flask

from app.commons.config import Config


class Context(object):
    """
    Context class
    """
    def __init__(self, logger: Flask.logger) -> None:
        self.logger = logger
        self.config = Config()
