from flask import Flask, jsonify, request
from flask_cors import CORS

from app.commons.config import Config
from app.commons.context import Context
from app.controllers.file_controller import FileController
from app.controllers.ocr_controller import OcrController
from app.middlewares.auth import Auth

API_VERSION = '/api/v1'

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route(API_VERSION + '/files/upload', methods=['POST'])
def files_upload():
    if request.method == 'POST':
        return FileController(Context(app.logger)).upload(request)
    return jsonify({})


@app.route(API_VERSION + '/files/ocr', methods=['POST'])
def files_ocr():
    if request.method == 'POST':
        return OcrController(Context(app.logger)).execute(request)
    return jsonify({})


@app.route(API_VERSION + '/login', methods=['POST'])
def login():
    result = Auth(Context(app.logger)).create(request)
    if request.method == 'POST':
        return jsonify({'message': 'login', 'result': result})
    return jsonify({})


@app.route(API_VERSION + '/signin', methods=['POST'])
def signin():
    result = Auth(Context(app.logger)).is_valid(request.headers)
    Auth().create(request.headers)
    if request.method == 'POST':
        return jsonify({'message': 'signin', 'result': result})
    return jsonify({})


@app.route(API_VERSION + '/singup', methods=['POST'])
def signup():
    result = Auth(Context(app.logger)).create(request)
    if request.method == 'POST':
        return jsonify({'message': 'signup', 'result': result})
    return jsonify({})


@app.route(API_VERSION + '/logout', methods=['DELETE'])
def logout():
    result = Auth(Context(app.logger)).delete(request.headers)
    if request.method == 'DELETE':
        return jsonify({'message': 'logout', 'result': result})
    return jsonify({})


@app.route('/', methods=['GET'])
def index():
    return {}


if __name__ == '__main__':
    app.secret_key = Config().APP_SECRET
    app.config['JSON_AS_ASCII'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.run(debug=True, host='0.0.0.0', port=5000)
