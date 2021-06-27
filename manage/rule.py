
import os

from git import Repo

from context.exception import BusinessError
from manage import _repo_dir, RULE_MARK, repo_push, FEATX_CODER
from service.model.template import Template
from service.model.template_rule import TemplateRule
from service.template import TemplateService
from service.template_rule import TemplateRuleService


class TemplateRuleManager:
    def __init__(self, services: dict, templates: str):
        self.__template_service: TemplateService = services["template"]
        self.__template_rule_service: TemplateRuleService = services["template-rule"]
        self.__git_templates = templates

    def __template(self, code: str):
        if code is None or code.strip() == "":
            raise BusinessError.PARAMETER_LOST.with_info("template_code")
        template = self.__template_service.find_by_code(code)
        if template is None:
            raise BusinessError.TEMPLATE_NOT_FOUND.with_info(code)
        return template

    def create(self, creating_rule):
        template = self.__template(creating_rule.template_code)
        template_dir = _repo_dir(self.__git_templates, template.repo_url)

        if creating_rule.path is not None and creating_rule.path.strip() != "":
            if _refactor_path(template_dir, creating_rule.path, True, template):
                creating_rule.path = creating_rule.path + RULE_MARK

        template_rule = self.__template_rule_service.create(_to_template_rule(creating_rule))
        return template_rule

    def update(self, updating_rule):
        if updating_rule.code is None or updating_rule.code.strip() == "":
            raise BusinessError.PARAMETER_LOST.with_info("code")
        rule = self.__template_rule_service.find_by_code(updating_rule.code)
        if rule is None:
            raise BusinessError.RULE_ENTITY_NOT_FOUND.with_info(updating_rule.code)
        template = self.__template(updating_rule.template_code)
        template_dir = _repo_dir(self.__git_templates, template.repo_url)

        if updating_rule.path is not None and updating_rule.path.strip() != "" and updating_rule.path != rule.path:
            if rule.path is not None and rule.path.strip() != "":
                _refactor_path(template_dir, rule.path, False, template)
            if _refactor_path(template_dir, updating_rule.path, True, template):
                updating_rule.path = updating_rule.path + RULE_MARK

        rule = self.__template_rule_service.update(_to_template_rule(updating_rule))
        return rule


def _to_template_rule(template_rule):
    return TemplateRule(
        code=template_rule.code,
        name=template_rule.name,
        type=template_rule.type,
        template_code=template_rule.template_code,
        path=template_rule.path,
        engine=template_rule.engine,
        data=template_rule.data,
        comment=template_rule.comment
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


def _refactor_path(abs_dir: str, rule_path: str, is_add: bool, template: Template):
    abs_rule_path = os.path.join(abs_dir, rule_path)
    if is_add and os.path.exists(abs_rule_path + RULE_MARK):
        return True
    elif not is_add and abs_rule_path.endswith(RULE_MARK) and os.path.exists(abs_rule_path[:-4]):
        return True

    path_update = False
    files = dict()

    if os.path.isfile(abs_rule_path):
        if is_add:
            path_update = not abs_rule_path.endswith(RULE_MARK)
        else:
            path_update = abs_rule_path.endswith(RULE_MARK)

    if is_add:
        _append_for_rule(abs_dir, rule_path, files)
    else:
        _remove_for_rule(abs_dir, rule_path, files)

    if len(files) > 0 and is_add:
        _commit_and_push(abs_dir, files, template)
    return path_update


def _append_for_rule(abs_dir: str, rule_path: str, result: dict):
    abs_rule_path = os.path.join(abs_dir, rule_path)
    if os.path.isfile(abs_rule_path) and not abs_rule_path.endswith(RULE_MARK):
        os.renames(abs_rule_path, abs_rule_path + RULE_MARK)
        result[rule_path] = rule_path + RULE_MARK
    elif os.path.isdir(abs_rule_path):
        for path in os.listdir(abs_rule_path):
            _append_for_rule(abs_dir, os.path.join(rule_path, path), result)


def _remove_for_rule(abs_dir: str, rule_path: str, result: dict):
    abs_rule_path = os.path.join(abs_dir, rule_path)
    if os.path.isfile(abs_rule_path) and abs_rule_path.endswith(RULE_MARK):
        os.renames(abs_rule_path, abs_rule_path[:-4])
        result[rule_path] = rule_path[:-4]
    elif os.path.isdir(abs_rule_path):
        for path in os.listdir(abs_rule_path):
            _remove_for_rule(abs_dir, os.path.join(rule_path, path), result)


def _commit_and_push(template_dir: str, files: dict, template: Template):
    repo = Repo(template_dir)

    try:
        repo.index.remove(files.keys())
        repo.index.add(files.values())
        repo.index.commit("rule files renamed", author=FEATX_CODER, committer=FEATX_CODER)

    except Exception as e:
        # TODO Logger Required
        pass
    repo_push(repo, template.repo_url, template.branch, template.api_token)
