from sqlalchemy import Column, String

from service.model import Update


class Language(Update):
    __tablename__ = "t_coder_language"
    code = Column(String(), default="", nullable=False)
    name = Column(String(), default="", nullable=False)
    comment = Column(String(), default="", nullable=False)
