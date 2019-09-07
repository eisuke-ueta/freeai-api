from typing import Any

from flask import jsonify

from app.commons.context import Context


class OcrController(object):
    def __init__(self, context: Context) -> None:
        self.context = context
        self.logger = context.logger
        self.config = context.config

    def execute(self, request: Any) -> str:
        return jsonify({})
