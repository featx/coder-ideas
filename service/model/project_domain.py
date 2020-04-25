
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from service.model import Unified


class ProjectDomain(declarative_base(), Unified):
    __tablename__ = "t_coder_project_domain"
    sort = Column(Integer(), default=0, nullable=False)
    project_code = Column(String(), default="", nullable=False)
    comment = Column(String(), default="", nullable=False)
