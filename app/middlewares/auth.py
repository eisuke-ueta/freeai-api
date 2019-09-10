import json
from typing import Any

import jwt
from flask import request

from app.commons.context import Context


class Auth(object):

    HS256 = 'HS256'

    def __init__(self, context: Context) -> None:
        self.context = context
        self.logger = context.logger
        self.config = context.config
        self.tokens = []

    def create(self, request: request) -> str:
        data = json.loads(request.data.decode('utf-8'))

        payload = {'email': data["email"]}
        token = jwt.encode(payload, self.config.APP_SECRET, algorithm=self.HS256).decode('utf-8')

        # TODO Save to database
        self.tokens.append(token)

        return token

    def delete(self, headers: Any) -> bool:
        token = self._get_token_from_headers(headers)
        self.logger.info(token)

        # TODO Delete from database
        self.tokens = []

        return True

    def validate(self, headers: Any) -> bool:
        token = self._get_token_from_headers(headers)

        if token not in self.tokens:
            raise Exception('token is not found')

        user = {'email': 'sample@gmail.com'}
        self.context.set_user(user)

        return True

    @staticmethod
    def _get_token_from_headers(headers: Any) -> str:
        authorization = headers["Authorization"]
        return authorization.split()[1]
