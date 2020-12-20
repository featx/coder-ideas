
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

    def override_by(self, template_rule):
        if template_rule.name is not None and template_rule.name.strip() != "":
            self.name = template_rule.name
        if template_rule.type is not None:
            self.type = template_rule.type
        if template_rule.sort is not None:
            self.sort = template_rule.sort
        if template_rule.template_code is not None and template_rule.template_code.strip() != "":
            self.template_code = template_rule.template_code
        if template_rule.engine is not None and template_rule.engine.strip() != "":
            self.engine = template_rule.engine
        if template_rule.data is not None and template_rule.data.strip() != "":
            self.data = template_rule.data
        if template_rule.comment is not None and template_rule.comment.strip() != "":
            self.comment = template_rule.comment