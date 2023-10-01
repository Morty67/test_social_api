__all__ = ["User"]

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime, onupdate=func.now())
    last_request = Column(DateTime, onupdate=func.now())
    hashed_password = Column(String)
    is_admin = Column(Boolean, server_default='False')

    posts = relationship("Post", back_populates="user")
    likes = relationship("Like", back_populates="user")
