from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from service.model import Unified


class DomainProperty(declarative_base(), Unified):
    __tablename__ = "t_coder_domain_property"
    sort = Column(Integer(), default=0, nullable=False)
    domain_code = Column(String(), default="", nullable=False)
    project_code = Column(String(), default="", nullable=False)
    comment = Column(String(), default="", nullable=False)
