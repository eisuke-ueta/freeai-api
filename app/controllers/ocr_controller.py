import json
from typing import Any

from flask import jsonify, abort

from app.commons.context import Context
from app.services.ocr_service import OcrService


class OcrController(object):
    def __init__(self, context: Context) -> None:
        self.context = context
        self.logger = context.logger
        self.config = context.config

    def execute(self, request: Any) -> str:
        self.logger.info("START")
        response = jsonify({})

        try:
            data = json.loads(request.data.decode('utf-8'))
            if 'image_url' not in data:
                abort(400, {'message': 'Image url does not exit'})

            image_url = data["image_url"]
            text = OcrService(self.context).execute(image_url)

            response = jsonify({'text': text})
        except Exception as e:
            self.logger.error(e)

        self.logger.info("END")
        return response
