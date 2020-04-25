from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from service.model import Unified


class DataEngine(declarative_base(), Unified):
    __tablename__ = "t_coder_data_engine"
    sort = Column(Integer(), default=0, nullable=False)
    image_url = Column(String(), default="", nullable=False)
    comment = Column(String(), default="", nullable=False)
