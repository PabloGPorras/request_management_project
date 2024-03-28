from sqlalchemy import Column, Integer, String

from utils.utils import Base


class Model(Base):
    """Table to store models"""
    __tablename__ = "models"
    __table_args__ = {}
    id = Column(Integer, primary_key=True)
    model_name = Column(String, nullable=False)
    model_json = Column(String, nullable=False)