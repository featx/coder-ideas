
from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

from service.model import Update


class Language(declarative_base(), Update):
    __tablename__ = "t_coder_language"
    code = Column(String(), default="", nullable=False)
    name = Column(String(), default="", nullable=False)
    sort = Column(Integer(), default=0, nullable=False)
    prop_types = Column(JSON(), default={}, nullable=False)
    comment = Column(String(), default="", nullable=False)
