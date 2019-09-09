from datetime import datetime

from sqlalchemy import BIGINT, DATETIME, Column, String
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class UserModel(BaseModel):
    __tablename__ = 'users'

    id = Column('id', BIGINT, primary_key=True)
    name = Column('name', String(255), nullable=False)
    email = Column('email', String(255), nullable=False, unique=True)
    password = Column('password', String(255), nullable=False)
    reset_password_token = Column('reset_password_token', String(255))
    reset_password_sent_at = Column('reset_password_sent_at', DATETIME)
    confirmation_token = Column('confirmation_token', String(255))
    confirmation_sent_at = Column('confirmation_sent_at', DATETIME)
    confirmed_at = Column('confirmed_at', DATETIME)
    created_at = Column('created_at',
                        DATETIME,
                        default=datetime.now,
                        nullable=False)
    updated_at = Column('updated_at', DATETIME, onupdate=datetime.now)
