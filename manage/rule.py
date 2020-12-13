from service.model.template_rule import TemplateRule
from service.template import TemplateService


class TemplateRuleManager:
    def __init__(self, services):
        self.__template_service: TemplateService = services["template"]

    def create(self, creating_rule):
        template = self.__template_service.find_by_code(creating_rule.template_code)
        project_template = self.__template_service.create(_to_template_rule(creating_rule))
        return project_template


def _to_template_rule(creating_rule):
    return TemplateRule(
        code=creating_rule.code,
        name=creating_rule.name,
        type=creating_rule.type,
        template_code=creating_rule.template_code,
        path=creating_rule.path,
        engine=creating_rule.engine,
        data=creating_rule.data,
        comment=creating_rule.comment
    )


def _from_template_rule(project_template):
    return {
        "code": project_template.code,
        "name": project_template.name,
        "project_code": project_template.project_code,
        "path": project_template.path,
        "engine": project_template.engine,
        "data": project_template.data,
        "comment": project_template.comment
    }