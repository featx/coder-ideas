from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Query

from service.model import Unified, Page, non_default


class Template(declarative_base(), Unified):
    __tablename__ = "t_coder_template"
    sort = Column(Integer(), default=0, nullable=False)
    language_code = Column(String(), default="", nullable=False)
    framework_code = Column(String(), default="", nullable=False)
    repo_url = Column(String(), default="", nullable=False)
    branch = Column(String(), default="", nullable=False)
    commit = Column(String(), default="", nullable=False)
    api_token = Column(String(), default="", nullable=False)
    comment = Column(String(), default="", nullable=False)

    def override_by(self, template):
        if template.name is not None and template.name.strip() != "":
            self.name = template.name
        if template.type is not None:
            self.type = template.type
        if template.sort is not None:
            self.sort = template.sort
        if template.language_code is not None and template.language_code.strip() != "":
            self.language_code = template.language_code
        if template.framework_code is not None and template.framework_code.strip() != "":
            self.framework_code = template.framework_code
        if template.branch is not None and template.branch.strip() != "":
            self.branch = template.branch
        if template.commit is not None and template.commit.strip() != "":
            self.commit = template.commit
        if template.api_token is not None and template.api_token.strip() != "":
            self.api_token = template.api_token
        if template.comment is not None and template.comment.strip() != "":
            self.comment = template.comment

class TemplatePageCriteria(Page):
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
                .filter(Template.code==self.code)
        if self.name is not None:
            query_result = non_default(query_result, query)\
                .filter(Template.name==self.name)
        return non_default(query_result, query)
