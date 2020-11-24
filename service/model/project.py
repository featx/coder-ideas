from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query

from service.model import Unified, Page


class Project(declarative_base(), Unified):
    __tablename__ = "t_coder_project"
    status = Column(Integer(), default=0, nullable=False)
    image_url = Column(String(), default="", nullable=False)
    language_code = Column(String(), default="", nullable=False)
    framework_code = Column(String(), default="", nullable=False)
    template_repo_url = Column(String(), default="", nullable=False)
    template_branch = Column(String(), default="", nullable=False)
    template_commit = Column(String(), default="", nullable=False)
    template_api_token = Column(String(), default="", nullable=False)
    repo_url = Column(String(), default="", nullable=False)
    branch = Column(String(), default="", nullable=False)
    api_token = Column(String(), default="", nullable=False)
    comment = Column(String(), default="", nullable=False)


class ProjectPageCriteria(Page):
    code = None
    name = None

    def __init__(self, dict):
        super().__init__(dict)

    def query(self, query: Query):
        if query is None:
            return None
        query_result = None
        if self.project_code is not None:
            query_result = non_default(query_result, query)\
                .filter(Project.code==self.project_code)
        if self.project_name is not None:
            query_result = non_default(query_result, query)\
                .filter(Project.name==self.project_name)
        return non_default(query_result, query)


def non_default(obj, d4t):
    if obj is None:
        return d4t
    return obj