from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.commons.config import Config
from app.models.session_model import SessionModel
from app.models.user_model import UserModel

Engine = create_engine(Config().MYSQL_URI, echo=True)
Session = sessionmaker(bind=Engine)

# Create tables
SessionModel.metadata.create_all(bind=Engine)
UserModel.metadata.create_all(bind=Engine)