from sqlalchemy import Column, Integer, String
from src.model import Unified


class Project(Unified):
    __tablename__ = "t_coder_project"
    status = Column(Integer(), default="", nullable=False)
    image_url = Column(String(), default="", nullable=False)
    language_code = Column(String(), default="", nullable=False)
    framework_code = Column(String(), default="", nullable=False)
    template_repo_url = Column(String(), default="", nullable=False)
    template_api_token = Column(String(), default="", nullable=False)
    repo_url = Column(String(), default="", nullable=False)
    api_token = Column(String(), default="", nullable=False)
    comment = Column(String(), default="", nullable=False)

class SavingProject():
    pass;
