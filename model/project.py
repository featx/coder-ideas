from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from model import Unified


class Project(declarative_base(), Unified):
    __tablename__ = "t_coder_project"
    status = Column(Integer(), default=0, nullable=False)
    image_url = Column(String(), default="", nullable=False)
    language_code = Column(String(), default="", nullable=False)
    framework_code = Column(String(), default="", nullable=False)
    template_repo_url = Column(String(), default="", nullable=False)
    template_api_token = Column(String(), default="", nullable=False)
    repo_url = Column(String(), default="", nullable=False)
    api_token = Column(String(), default="", nullable=False)
    comment = Column(String(), default="", nullable=False)
