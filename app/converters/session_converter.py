from app.models.session_model import SessionModel


class SessionConverter(object):
    def get_model_object(self, token: str) -> dict:
        return {"token": token}

    def get_value_object(self, session_model: SessionModel) -> dict:
        return {"token": session_model.token}
