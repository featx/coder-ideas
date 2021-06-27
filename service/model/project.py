from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query

from service.model import Unified, Page, non_default


class Project(declarative_base(), Unified):
    __tablename__ = "t_coder_project"
    status = Column(Integer(), default=0, nullable=False)
    image_url = Column(String(), default="", nullable=False)
    template_code = Column(String(), default="", nullable=False)
    repo_url = Column(String(), default="", nullable=False)
    branch = Column(String(), default="", nullable=False)
    api_token = Column(String(), default="", nullable=False)
    variables = Column(JSON(), default={}, nullable=False)
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
        if self.code is not None:
            query_result = non_default(query_result, query)\
                .filter(Project.code==self.code)
        if self.name is not None:
            query_result = non_default(query_result, query)\
                .filter(Project.name==self.name)
        return non_default(query_result, query)
