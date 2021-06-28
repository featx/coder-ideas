import os

from context.exception import BusinessError
from manage import _repo_dir, _render_domain_files, repo_add, _render_project

from service.model.domain_property import DomainProperty
from service.model.project_domain import ProjectDomain

from service.template import TemplateService
from service.template_rule import TemplateRuleService
from service.project import ProjectService
from service.project_domain import ProjectDomainService
from service.domain_property import DomainPropertyService


class DomainManager:
    def __init__(self, services, templates: str, workspace: str):
        self.__template_service: TemplateService = services["template"]
        self.__template_rule_service: TemplateRuleService = services["template-rule"]
        self.__project_service: ProjectService = services["project"]
        self.__domain_service: ProjectDomainService = services["project-domain"]
        self.__domain_property_service: DomainPropertyService = services["domain-property"]
        self.__git_workspace = workspace
        self.__git_templates = templates

    def create(self, creating_domain):
        project = self.__project_service.find_by_code(creating_domain.project_code)
        if project is None:
            raise BusinessError.PROJECT_NOT_FOUND.with_info(creating_domain.project_code)
        domain = self.__domain_service.create(_to_project_domain(creating_domain))
        domain_properties = []
        for prop in creating_domain.properties:
            prop.domain_code = domain.code
            prop.project_code = creating_domain.project_code
            domain_properties.append(_to_domain_property(prop))
        self.__domain_property_service.create(domain_properties)

        domain.properties = domain_properties
        domain.project = project
        self.__domain_add_to_project(domain, project.template_code)

        return domain

    def __domain_add_to_project(self, domain: ProjectDomain, template_code: str):
        template = self.__template_service.find_by_code(template_code)
        rules = self.__template_rule_service.find_by_template_code(template.code)
        template_dir = _repo_dir(self.__git_templates, template.repo_url)
        project_dir = os.path.join(self.__git_workspace, domain.project_code)

        files_to_add = []
        for rule in rules:
            rule.data["${language.code}"] = template.language_code
            rule_data = _render_project(rule.data, domain.project)
            rule_path = os.path.join(template_dir, rule.path)
            domain_path = os.path.join(project_dir, rule.path)
            if os.path.isfile(rule_path):
                files_to_add += _render_domain_files(rule_path, domain_path, rule_data, [domain])
            elif os.path.isdir(rule_path):
                for _file in os.listdir(rule_path):
                    rule_file = os.path.join(rule_path, _file)
                    domain_file = os.path.join(domain_path, _file)
                    files_to_add += _render_domain_files(rule_file, domain_file, rule_data, [domain])
        if len(files_to_add) > 0:
            repo_add(project_dir, files_to_add)


def _to_project_domain(creating_domain):
    return ProjectDomain(
        code=creating_domain.code,
        name=creating_domain.name,
        type=creating_domain.type,
        project_code=creating_domain.project_code,
        comment=creating_domain.comment
    )


def _to_domain_property(domain_property):
    return DomainProperty(
        code=domain_property.code,
        name=domain_property.name,
        type=domain_property.type,
        domain_code=domain_property.domain_code,
        project_code=domain_property.project_code,
        comment=domain_property.comment
    )
