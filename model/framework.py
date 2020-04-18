from sqlalchemy import Column, String

from src.model import Update


class Framework(Update):
    __tablename__ = "t_coder_framework"
    code = Column(String(), default="", nullable=False)
    name = Column(String(), default="", nullable=False)
    alias = Column(String(), default="", nullable=False)
    comment = Column(String(), default="", nullable=False)
