from app.commons.context import Context


class OcrService(object):
    def __init__(self, context: Context) -> None:
        self.context = context

    def execute(self, input_data: dict) -> dict:
        return {}
