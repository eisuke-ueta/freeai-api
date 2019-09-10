from datetime import datetime

from sqlalchemy import BIGINT, DATETIME, Column, String
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class SessionModel(BaseModel):
    __tablename__ = 'sessions'

    id = Column('id', BIGINT, primary_key=True)
    token = Column('token', String(255), nullable=False, unique=True)
    created_at = Column('created_at', DATETIME, default=datetime.now, nullable=False)
