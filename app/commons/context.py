from flask import Flask

from app.commons.config import Config
from app.middlewares.database import Session


class Context(object):
    """
    Context class
    """
    def __init__(self, logger: Flask.logger) -> None:
        self.logger = logger
        self.config = Config()
        self.user = {}
        self.session = Session()

    def set_user(self, user: dict) -> None:
        self.user = user
