from app.models.user_model import UserModel


class UserConverter(object):

    def get_model_object(self, data: dict) -> dict:
        return {
            "name": data["name"],
            "email": data["email"],
            "password": data["password"]
        }

    def get_value_object(self, user_model: UserModel) -> dict:
        return {
            "name": user_model.name,
            "email": user_model.email
        }
