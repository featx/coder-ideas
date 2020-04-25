
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from service.model import Update


class ProjectDateEngine(declarative_base(), Update):
    __tablename__ = "t_coder_project_data_engine"
    code = Column(String(), unique=True, default="", nullable=False)
    project_code = Column(String(), default="", nullable=False)
    data_engine_code = Column(String(), default="", nullable=False)
    sort = Column(Integer(), default=0, nullable=False)
    comment = Column(String(), default="", nullable=False)
