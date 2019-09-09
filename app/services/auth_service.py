from flask_bcrypt import Bcrypt
import jwt

from app.commons.context import Context
from app.converters.user_converter import UserConverter
from app.converters.session_converter import SessionConverter
from app.repositories.user_repository import UserRepository
from app.repositories.session_repository import SessionRepository


class AuthService(object):

    HS256 = "HS256"
    UTF8 = "utf-8"

    def __init__(self, context: Context) -> None:
        self.context = context
        self.logger = context.logger
        self.config = context.config
        self.bcrypt = Bcrypt()

    def login(self, email: str, password: str) -> str:
        
        # Get user data
        user_model = UserRepository(self.context).find_by_email(email)

        is_valid = self.bcrypt.check_password_hash(user_model.password, password)
        if not is_valid:
            self.logger.info("Provided password is not correct.")
            return None

        # Create session

        return UserConverter().get_value_object(user_model)

    def signin(self, token: str) -> bool:
        return True

    def signup(self, data: dict) -> dict:
        # Prepare model data
        data["password"] = self.bcrypt.generate_password_hash(data["password"]).decode(self.UTF8)
        payload = {'email': data["email"]}
        token = jwt.encode(payload,
                           self.config.APP_SECRET,
                           algorithm=self.HS256).decode(self.UTF8)

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

    def logout(self, token: str) -> bool:
        return True