from sqlalchemy import Column, Integer, String
from utils.utils import Base


class User(Base):
    """Table to store user data"""
    __tablename__ = "user"
    __table_args__ = {}
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String, nullable=False)
    user_role = Column(String, nullable=False, default="user")
    email_from = Column(String, nullable=False)
    email_to = Column(String, nullable=False)
    email_cc = Column(String, nullable=False)
    

