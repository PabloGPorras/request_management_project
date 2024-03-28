from sqlalchemy import Column, Integer, String

from utils.utils import Base


class Configuration(Base):
    """Table to store configurations"""
    __tablename__ = "configuration"
    __table_args__ = {}
    id = Column(Integer, primary_key=True)
    tool_version = Column(String, nullable=False)
    json = Column(String, nullable=False)