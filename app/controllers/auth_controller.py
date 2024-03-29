import json
from typing import Any

from flask import abort, jsonify

from app.commons.context import Context
from app.services.auth_service import AuthService


class AuthController(object):
    def __init__(self, context: Context) -> None:
        self.context = context
        self.logger = context.logger
        self.config = context.config

    def login(self, request: Any) -> str:
        try:
            if request.method != 'POST':
                return jsonify({})

            data = json.loads(request.data.decode('utf-8'))
            if 'email' not in data or 'password' not in data:
                abort(400, {'message': 'Incorrect form submission'})

            email = data["email"]
            password = data["password"]
            response = AuthService(self.context).login(email, password)

            return jsonify(response)
        except Exception as e:
            self.logger.error(e)
            abort(500, {'message': 'Failed to login ...'})

    def signin(self, request: Any) -> str:
        try:
            if request.method != 'POST':
                return jsonify({})

            authorization = request.headers["Authorization"]
            if not authorization:
                abort(400, {'message': 'Authorization does not exist.'})

            token = authorization.split()[1]
            response = AuthService(self.context).signin(token)

            if not response:
                abort(403, {'message': 'Not authorized.'})

            return jsonify(response)
        except Exception as e:
            self.logger.error(e)
            abort(500, {'message': 'Failed to signin ...'})

    def signup(self, request: Any) -> str:
        try:
            if request.method != 'POST':
                return jsonify({})

            data = json.loads(request.data.decode('utf-8'))
            if 'email' not in data or 'name' not in data or 'password' not in data:
                abort(400, {'message': 'Incorrect form submission'})

            response = AuthService(self.context).signup(data)

            return jsonify(response)
        except Exception as e:
            self.logger.error(e)
            abort(500, {'message': 'Failed to signup ...'})

    def logout(self, request: Any) -> str:
        try:
            if request.method != 'DELETE':
                return jsonify({})

            authorization = request.headers["Authorization"]
            if not authorization:
                abort(400, {'message': 'Authorization does not exist.'})

            token = authorization.split()[1]
            response = AuthService(self.context).logout(token)

            if not response:
                abort(403, {'message': 'Not authorized.'})

            return jsonify(response)
        except Exception as e:
            self.logger.error(e)
            abort(500, {'message': 'Failed to logout ...'})
