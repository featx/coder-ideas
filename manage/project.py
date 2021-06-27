import os

from git import Repo

from context.exception import BusinessError
from manage import _repo_dir, _copy_and_replace, _replace_data, delete_dir, \
    repo_copy, repo_commit_push, snake_camel, RULE_MARK
from manage.domain import _from_project_domain
from service.model.project_domain import ProjectDomain
from service.project_domain import ProjectDomainService
from service.model.project import Project, ProjectPageCriteria
from service.project import ProjectService
from service.template import TemplateService
from service.template_rule import TemplateRuleService


class ProjectManager:
    def __init__(self, services, templates: str, workspace: str):
        self.__project_service: ProjectService = services["project"]
        self.__template_service: TemplateService = services["template"]
        self.__template_rule_service: TemplateRuleService = services["template-rule"]
        self.__domain_service: ProjectDomainService = services["project-domain"]
        self.__git_workspace = workspace
        self.__git_templates = templates

    def create(self, creating_project):
        if creating_project.template_code is None or creating_project.template_code.strip() == "":
            raise BusinessError.PARAMETER_LOST.with_info("template_code")
        template = self.__template_service.find_by_code(creating_project.template_code)
        if template is None:
            raise BusinessError.TEMPLATE_NOT_FOUND.with_info(creating_project.template_code)
        project = self.__project_service.create(_to_project(creating_project))

        template_dir = _repo_dir(self.__git_templates, template.repo_url)
        project_dir = os.path.join(self.__git_workspace, project.code)
        repo_copy(template_dir, project_dir, template.default_rule)

        return project

    def update(self, param):
        if param.project_code is None or param.project_code.strip() != "":
            raise BusinessError.PARAMETER_LOST.with_info("project_code")
        project = self.__project_service.find_by_code(param.project_code)
        if project is None:
            raise BusinessError.PROJECT_NOT_FOUND.with_info(param.project_code)
        return self.__project_service.update(_to_project(param))

    def delete(self, project_code):
        delete_dir(os.path.join(self.__git_workspace, project_code))
        self.__project_service.delete(project_code)

    def get(self, project_code):
        project = self.__project_service.find_by_code(project_code)
        return _from_project(project)

    def detail(self, project_code: str):
        project = self.__project_service.find_by_code(project_code)
        result = _from_project(project)
        domains = self.__domain_service.find_by_project_code(project_code)
        result["domains"] = []
        for domain in domains:
            result["domains"].append(_from_project_domain(domain))
        return result

    def page(self, kv_map: dict):
        count, result_list = self.__project_service.find_by_page_criteria(ProjectPageCriteria(kv_map))
        result = []
        for project in result_list:
            result.append(_from_project(project))
        return {
            "total": count,
            "size": len(result_list),
            "page": kv_map["page"],
            "data": result
        }

    def generate(self, param):
        project, domains, template, rules = self.__find_project_domains_rules(param)
        template_dir = _repo_dir(self.__git_templates, template.repo_url)
        project_dir = os.path.join(self.__git_workspace, project.code)
        
        files_to_add = []
        for rule in rules:
            rule.data["${language.code}"] = template.language_code
            rule_path = os.path.join(template_dir, rule.path)
            domain_path = os.path.join(project_dir, rule.path)
            if os.path.isfile(rule_path):
                files_to_add += _render_domain_files(rule_path, domain_path, rule.data, domains)
            elif os.path.isdir(rule_path):
                for _file in os.listdir(rule_path):
                    rule_file = os.path.join(rule_path, _file)
                    domain_file = os.path.join(domain_path, _file)
                    files_to_add += _render_domain_files(rule_file, domain_file, rule.data, domains)
        if len(files_to_add) > 0:
            repo = Repo(project_dir)
            repo.index.add(files_to_add)

    def __find_project_domains_rules(self, param):
        if param.code is None or param.code.strip() == "":
            if param.domain_code is None or param.domain_code.strip() == "":
                raise BusinessError.PARAMETER_LOST.with_info("code or domain_code")
            domain = self.__domain_service.find_by_code(param.domain_code)
            if domain is None:
                raise BusinessError.DOMAIN_NOT_FOUND.with_info(param.domain_code)
            domains = [domain]
            project = self.__project_service.find_by_code(domain.project_code)
        else:
            project = self.__project_service.find_by_code(param.code)
            if project is None:
                raise BusinessError.PROJECT_NOT_FOUND.with_info(param.code)
            domains = self.__domain_service.find_by_project_code(param.code)

        if domains is None or len(domains) == 0 or project is None:
            raise BusinessError.NOTHING_TO_GENERATE.with_info("no domains")

        template = self.__template_service.find_by_code(project.template_code)
        if template is None:
            raise BusinessError.TEMPLATE_NOT_FOUND.with_info(project.template_code)
        if param.rule_code is None or param.rule_code.strip() == "":
            rules = self.__template_rule_service.find_by_template_code(template.code)
            if rules is None or len(rules) == 0:
                raise BusinessError.NOTHING_TO_GENERATE.with_info("no rules")
        else:
            rule = self.__template_rule_service.find_by_code(param.rule_code)
            if rule is None:
                raise BusinessError.RULE_NOT_FOUND.with_info(param.rule_code)
            rules = [rule]
        return project, domains, template, rules

    def commit_push(self, param):
        if param.project_code is None or param.project_code.strip() == "":
            raise BusinessError.PARAMETER_LOST.with_info("project_code")
        project = self.__project_service.find_by_code(param.project_code)
        if project is None:
            raise BusinessError.PROJECT_NOT_FOUND.with_info(param.project_code)
        project_dir = os.path.join(self.__git_workspace, project.code)
        repo_commit_push(project_dir, project.repo_url, project.branch, project.api_token)


def _to_project(creating_project):
    return Project(
        code=creating_project.code,
        name=creating_project.name,
        type=creating_project.type,
        image_url=creating_project.image_url,
        template_code=creating_project.template_code,
        repo_url=creating_project.repo_url,
        api_token=creating_project.api_token,
        branch=creating_project.branch,
        comment=creating_project.comment
    )


def _from_project(project: Project):
    return {
        "id": project.id,
        "code": project.code,
        "name": project.name,
        "type": project.type,
        "status": project.status,
        "image_url": project.image_url,
        "template_code": project.template_code,
        "repo_url": project.repo_url,
        "branch": project.branch,
        "comment": project.comment
    }


def _render_data(template: dict, domain: ProjectDomain):
    data = dict()
    for key, value in template.items():
        k = key.replace("${domain.name|camel}", domain.name)
        k = k.replace("${domain.name|Camel}", domain.name)
        k = k.replace("${domain.name|snake}", snake_camel(domain.name))
        v = value.replace("${domain.name|camel}", domain.name)
        v = v.replace("${domain.name|Camel}", domain.name)
        v = v.replace("${domain.name|snake}", snake_camel(domain.name))
        data[k] = v
    if hasattr(domain, "properties"):
        data["properties"] = domain.properties
    return data


def _render_domain_files(rule_path: str, domain_path: str, data, domains: list):
    domain_files = []
    for domain in domains:
        data = _render_data(data, domain)
        domain_file = _replace_data(domain_path, data)
        if domain_file.endswith(RULE_MARK):
            domain_file = domain_file[:-4]
        data["properties"] = domain.properties
        _copy_and_replace(rule_path, domain_file, data)
        domain_files.append(domain_file)
    return domain_files
