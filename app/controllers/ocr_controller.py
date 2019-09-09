import json
from typing import Any

from flask import abort, jsonify

from app.commons.context import Context
from app.services.ocr_service import OcrService


class OcrController(object):
    def __init__(self, context: Context) -> None:
        self.context = context
        self.logger = context.logger
        self.config = context.config

    def execute(self, request: Any) -> str:
        try:
            if request.method != 'POST':
                return jsonify({})

            data = json.loads(request.data.decode('utf-8'))
            if 'image_url' not in data:
                abort(400, {'message': 'Image url does not exit'})

            image_url = data["image_url"]
            text = OcrService(self.context).execute(image_url)

            return jsonify({'text': text})
        except Exception as e:
            self.logger.error(e)
            abort(500, {'message': e.message})
