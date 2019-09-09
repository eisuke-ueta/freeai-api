from flask import Flask, jsonify, request
from flask_cors import CORS

from app.commons.config import Config
from app.commons.context import Context
from app.controllers.auth_controller import AuthController
from app.controllers.file_controller import FileController
from app.controllers.ocr_controller import OcrController
from app.middlewares.auth import Auth

API_VERSION = '/api/v1'

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route(API_VERSION + '/files/upload', methods=['POST'])
def files_upload():
    return FileController(Context(app.logger)).upload(request)

@app.route(API_VERSION + '/files/ocr', methods=['POST'])
def files_ocr():
    return OcrController(Context(app.logger)).execute(request)

@app.route(API_VERSION + '/login', methods=['POST'])
def login():
    return AuthController(Context(app.logger)).login(request)


@app.route(API_VERSION + '/signin', methods=['POST'])
def signin():
    return AuthController(Context(app.logger)).signin(request)


@app.route(API_VERSION + '/signup', methods=['POST'])
def signup():
    return AuthController(Context(app.logger)).signup(request)


@app.route(API_VERSION + '/logout', methods=['DELETE'])
def logout():
    return AuthController(Context(app.logger)).logout(request)


@app.route('/', methods=['GET'])
def index():
    return {}


if __name__ == '__main__':
    app.secret_key = Config().APP_SECRET
    app.config['JSON_AS_ASCII'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.run(debug=True, host='0.0.0.0', port=5000)
