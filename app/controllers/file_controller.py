from typing import Any

from flask import abort, jsonify

from app.commons.context import Context
from app.services.file_service import FileService
from app.services.ocr_service import OcrService


class FileController(object):
    def __init__(self, context: Context) -> None:
        self.context = context
        self.logger = context.logger
        self.config = context.config

    def upload(self, request: Any) -> str:
        self.logger.info("START")
        try:
            if request.method != 'POST':
                return jsonify({})

            if 'file' not in request.files:
                abort(400, {'message': 'File does not exit'})

            fileStorageObj = request.files['file']
            file_urls = FileService(self.context).upload(fileStorageObj)

            return jsonify({'urls': file_urls})
        except Exception as e:
            self.logger.error(e)
            abort(500, {'message': e.message})

    def delete(self, id: str) -> str:
        return FileService(self.context).delete(id)

    def ocr(self, input_data: dict) -> str:
        return OcrService(self.context).execute(input_data)
