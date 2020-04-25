
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from service.model import Update


class Framework(declarative_base(), Update):
    __tablename__ = "t_coder_framework"
    code = Column(String(), default="", nullable=False)
    name = Column(String(), default="", nullable=False)
    alias = Column(String(), default="", nullable=False)
    comment = Column(String(), default="", nullable=False)
