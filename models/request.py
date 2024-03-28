

from sqlalchemy import Column, Integer, String
from utils.utils import Base


class Request(Base):
    """Table to store request data"""
    __tablename__ = "request"
    __table_args__ = {}

    request_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False)
    request_type = Column(String, nullable=False)
    request_status = Column(String, nullable=False)
    requester = Column(String, nullable=False)
    team = Column(String, nullable=False)
    business_unit = Column(String, nullable=False)
    request_recieved_timestamp = Column(String, nullable=False)
    effort = Column(String, nullable=False)
    approval_timestamp = Column(String, nullable=False)
    approved_by = Column(String, nullable=False)
    approved = Column(String, nullable=False)
    govered_timestamp = Column(String, nullable=False)
    governed_by = Column(String, nullable=False)
    governed = Column(String, nullable=False)
    tool_version = Column(String, nullable=False)
    