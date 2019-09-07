from flask import Flask, jsonify, request
from flask_cors import CORS

from app.commons.config import Config
from app.commons.context import Context
from app.controllers.file_controller import FileController

API_VERSION = '/api/v1'

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route(API_VERSION + '/files/upload', methods=['POST'])
def files_upload():
    if request.method == 'POST':
        context = Context(app.logger)
        result = FileController(context).upload(request)
        return result
    return jsonify({})


@app.route(API_VERSION + '/files/ocr', methods=['POST'])
def files_ocr():
    input_data = request.data
    print(input_data)
    return {}


@app.route('/', methods=['GET'])
def index():
    return {}


if __name__ == '__main__':
    app.secret_key = Config().APP_SECRET
    app.config['JSON_AS_ASCII'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.run(debug=True, host='0.0.0.0', port=5000)
