from flask import Flask

from app.commons.context import Context
from app.services.file_service import FileService


def test_file_delete_succeed():
    context = Context(Flask.logger)
    result = FileService(context).delete('aaaa')
    assert type(result) == str
