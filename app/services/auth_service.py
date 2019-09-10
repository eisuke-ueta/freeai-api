import jwt
from flask_bcrypt import Bcrypt

from app.commons.context import Context
from app.converters.session_converter import SessionConverter
from app.converters.user_converter import UserConverter
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository


class AuthService(object):

    HS256 = "HS256"
    UTF8 = "utf-8"

    def __init__(self, context: Context) -> None:
        self.context = context
        self.logger = context.logger
        self.config = context.config
        self.bcrypt = Bcrypt()

    def login(self, email: str, password: str) -> dict:
        # Get user data
        user_model = UserRepository(self.context).find_by_email(email)
        if not user_model:
            self.logger.info("User does not exit. email: {}".format(email))
            return None

        # Check password
        is_valid = self.bcrypt.check_password_hash(user_model.password, password)
        if not is_valid:
            self.logger.info("Provided password is not correct. email: {}".format(email))
            return None

        # Create session
        token = self._encode_token(email)

        session_repository = SessionRepository(self.context)
        session_model = session_repository.find_by_token(token)
        if session_model:
            self.logger.info("Delete old session. token: {}".format(token))
            session_repository.delete(session_model)
            session_repository.save()

        session_object = SessionConverter().get_model_object(token)
        session_model = session_repository.create(session_object)
        session_repository.save()

        return {
            "user": UserConverter().get_value_object(user_model),
            'session': SessionConverter().get_value_object(session_model)
        }

    def signin(self, token: str) -> dict:
        # Get session object
        session_repository = SessionRepository(self.context)
        session_model = session_repository.find_by_token(token)

        # TODO Check create datetime

        # Decode token
        email = self._decode_token(token)

        # Get user object
        user_repository = UserRepository(self.context)
        user_model = user_repository.find_by_email(email)
        if not user_model:
            self.logger.info("User does not exit. token: {}".format(token))
            return None

        return {
            'user': UserConverter().get_value_object(user_model),
            'session': SessionConverter().get_value_object(session_model)
        }

    def signup(self, data: dict) -> dict:
        # Prepare model data
        data["password"] = self.bcrypt.generate_password_hash(data["password"]).decode(self.UTF8)
        token = self._encode_token(data["email"])

        user_object = UserConverter().get_model_object(data)
        session_object = SessionConverter().get_model_object(token)

        # Insert into database
        user_repository = UserRepository(self.context)
        user_model = user_repository.create(user_object)

        session_repository = SessionRepository(self.context)
        session_model = session_repository.create(session_object)

        # Commit
        user_repository.save()
        session_repository.save()

        return {
            'user': UserConverter().get_value_object(user_model),
            'session': SessionConverter().get_value_object(session_model)
        }

    def logout(self, token: str) -> dict:
        # Delete session
        session_repository = SessionRepository(self.context)
        session_model = session_repository.find_by_token(token)
        if not session_model:
            self.logger.info("Session does not exit. token: {}".format(token))
            return None
        session_repository.delete(session_model)
        session_repository.save()
        return {'success': True}

    def _encode_token(self, email: str) -> str:
        payload = {'email': email}
        token = jwt.encode(payload, self.config.APP_SECRET, algorithm=self.HS256).decode(self.UTF8)
        return token

    def _decode_token(self, token: str) -> str:
        payload = jwt.decode(token.encode(self.UTF8), self.config.APP_SECRET, algorithm=self.HS256)
        return payload["email"]
