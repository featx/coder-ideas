
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

from service.model import Unified


class TemplateRule(declarative_base(), Unified):
    __tablename__ = "t_coder_template_rule"
    sort = Column(Integer(), default=0, nullable=False)
    template_code = Column(String(), default="", nullable=False)
    path = Column(String(), default="", nullable=False)
    engine = Column(Integer(), default=0, nullable=False)
    data = Column(JSON(), nullable=False)
    comment = Column(String(), default="", nullable=False)
