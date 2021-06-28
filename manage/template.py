from context.exception import BusinessError
from manage import _repo_dir, repo_clone_checkout, repo_checkout, repo_pull
from service.model.template import Template, TemplatePageCriteria
from service.model.template_rule import TemplateRule
from service.template import TemplateService
from service.template_rule import TemplateRuleService


class TemplateManager:
    def __init__(self, services, templates: str):
        self.__template_service: TemplateService = services["template"]
        self.__template_rule_service: TemplateRuleService = services["template-rule"]
        self.__git_templates = templates

    def create(self, creating_template):
        local_dir = _repo_dir(self.__git_templates, creating_template.repo_url)
        creating_template.commit = \
            repo_clone_checkout(creating_template.repo_url, creating_template.api_token, local_dir, creating_template.branch)
        return self.__template_service.create(_to_template(creating_template))

    def update(self, updating_template):
        if updating_template.code is None or updating_template.code.strip() == "":
            raise Exception("Parameter code required")
        template = self.__template_service.find_by_code(updating_template.code)
        if template is None:
            raise Exception("Template not found")
        if updating_template.branch is not None and updating_template.branch.strip() != "" \
                and updating_template.branch != template.branch:
            #TODO The case of updating_template.repo_url != template.repo_url
            local_dir = _repo_dir(self.__git_templates, template.repo_url)
            updating_template.commit = repo_checkout(local_dir, updating_template.branch)
        return self.__template_service.update(_to_template(updating_template))

    def delete(self, code):
        self.__template_service.delete(code)

    def __template(self, code: str):
        if code is None or code.strip() == "":
            raise BusinessError.PARAMETER_LOST.with_info("code")
        template = self.__template_service.find_by_code(code)
        if template is None:
            raise BusinessError.TEMPLATE_NOT_FOUND.with_info(code)
        return template

    def get(self, template_code: str):
        template = self.__template(template_code)
        return _from_template(template)

    def detail(self, code: str):
        template = self.__template(code)
        template_info = _from_template(template)
        template_info["rules"] = []

        rules = self.__template_rule_service.list_of(code)
        if rules is None or len(rules) == 0:
            return template_info
        for rule in rules:
            template_info["rules"].append(_from_template_rule(rule))

        return template_info

    def page(self, kv_map):
        count, result_list = self.__template_service.find_by_page_criteria(TemplatePageCriteria(kv_map))
        result = []
        for template in result_list:
            result.append(_from_template(template))
        return {
            "total": count,
            "size": len(result_list),
            "page": kv_map["page"],
            "data": result
        }

    def list_all(self):
        result = []
        templates = self.__template_service.list_all()
        for template in templates:
            result.append(_from_template(template))
        return result

    def pull_repo(self, body):
        template = self.__template_service.find_by_code(body['template_code']
                                                        if body.__contains__('template_code') else body['code'])
        local_dir = _repo_dir(self.__git_templates, template.repo_url)
        return repo_pull(local_dir)


def _to_template(creating_template):
    return Template(
        code=creating_template.code,
        name=creating_template.name,
        type=creating_template.type,
        sort=creating_template.sort,
        language_code=creating_template.language_code,
        framework_code=creating_template.framework_code,
        repo_url=creating_template.repo_url,
        api_token=creating_template.api_token,
        default_rule=creating_template.default_rule,
        branch=creating_template.branch,
        commit=creating_template.commit,
        comment=creating_template.comment
    )


def _from_template(template: Template):
    return {
        "id": template.id,
        "code": template.code,
        "name": template.name,
        "type": template.type,
        "language_code": template.language_code,
        "framework_code": template.framework_code,
        "repo_url": template.repo_url,
        "branch": template.branch,
        "commit": template.commit,
        "default_rule": template.default_rule,
        "comment": template.comment
    }


def _from_template_rule(template_rule: TemplateRule):
    return {
        "code": template_rule.code,
        "name": template_rule.name,
        "template_code": template_rule.template_code,
        "path": template_rule.path,
        "engine": template_rule.engine,
        "data": template_rule.data,
        "comment": template_rule.comment
    }