import os

from git import Repo

from plugin import delete_dir
from plugin.language_type import dict_type_by_lang_code
from service.project_domain import ProjectDomainService
from service.model.project import Project
from service.project import ProjectService
from service.project_template import ProjectTemplateService


def _repo_with_token_url(url, api_token):
    if url is None:
        return None

    schema = "https"

    if api_token is None:
        api_token = ""
    else:
        api_token = "{}@".format(api_token)

    path = url
    if url.startswith("https"):
        path = url[8:]
    elif url.startswith("http"):
        schema = "http"
        path = url[7:]
    return "{}://{}{}".format(schema, api_token, path)


class ProjectManager:
    def __init__(self, services, workspace):
        self.__project_service: ProjectService = services["project"]
        self.__template_service: ProjectTemplateService = services["project-template"]
        self.__domain_service: ProjectDomainService = services["project-domain"]
        self.__git_workspace = workspace

    def create(self, creating_project):
        repo_dir = os.path.join(self.__git_workspace, creating_project.name)

        # Clone from template project
        url = _repo_with_token_url(creating_project.template_repo_url, creating_project.template_api_token)
        repo = Repo.clone_from(url, repo_dir, branch=creating_project.template_branch)
        creating_project.template_commit = repo.head.commit.hexsha
        repo.close()
        delete_dir(os.path.join(repo_dir, ".git"))

        project = self.__project_service.create(_to_project(creating_project))

        project_dir = os.path.join(self.__git_workspace, project.code)
        os.rename(repo_dir, project_dir)
        Repo.init(project_dir).close()
        return project

    def update(self, param):
        pass

    def delete(self, project_code):
        self.__project_service.delete(project_code)

    def get(self, project_code):
        project = self.__project_service.delete(project_code)
        # Refactor project as provided properties
        return project

    def detail(self, project_code: str):
        project = self.__project_service.find_by_code(project_code)
        templates = self.__template_service.find_by_project_code(project_code)
        domains = self.__domain_service.find_by_project_code(project_code)

    def page(self, project_code):
        pass

    def generate(self, param):
        project, domains, templates = self.__find_project_domains_templates(param)
        if project is None:
            return
        project_dir = os.path.join(self.__git_workspace, project.code)
        for template in templates:
            template.data["${language.code}"] = project.language_code
            template_path = os.path.join(project_dir, template.path)
            if os.path.isfile(template_path):
                template_file = template_path
                _render_domain_files(template, template_file, domains)
            elif os.path.isdir(template_path):
                for _file in os.listdir(template_path):
                    template_file = os.path.join(template_path, _file)
                    _render_domain_files(template, template_file, domains)

    def __find_project_domains_templates(self, param):
        domain = None
        template = None
        if hasattr(param, 'domain_code'):
            domain = self.__domain_service.find_by_code(param.domain_code)
        if hasattr(param, 'template_code'):
            template = self.__template_service.find_by_code(param.template_code)
        domains = []
        templates = []
        if domain is None and template is None:
            project = self.__project_service.find_by_code(param.project_code)
            if project is None:
                return None, None, None
            domains = self.__domain_service.find_by_project_code(param.project_code)
            templates = self.__template_service.find_by_project_code(param.project_code)
        elif domain is None:
            project = self.__project_service.find_by_code(template.project_code)
            domains = self.__domain_service.find_by_project_code(param.project_code)
            templates.append(template)
        elif template is None:
            project = self.__project_service.find_by_code(domain.project_code)
            domains.append(domain)
            templates = self.__template_service.find_by_project_code(param.project_code)
        else:
            project = self.__project_service.find_by_code(domain.project_code)
            domains.append(domain)
            templates.append(template)
        return project, domains, templates


def _to_project(creating_project):
    return Project(
        code=creating_project.code,
        name=creating_project.name,
        image_url=creating_project.image_url,
        template_repo_url=creating_project.template_repo_url,
        template_api_token=creating_project.template_api_token,
        template_branch=creating_project.template_branch,
        template_commit=creating_project.template_commit,
        repo_url=creating_project.repo_url,
        api_token=creating_project.api_token,
        branch=creating_project.branch,
        comment=creating_project.comment
    )


def _render_data(template: dict, domain):
    data = dict()
    for key, value in template.items():
        k = key.replace("${domain.name}", domain.name)
        v = value.replace("${domain.name}", domain.name)
        data[k] = v
    if hasattr(domain, "properties"):
        data["properties"] = domain.properties
    return data


def _replace_data(origin: str, data: dict):
    result = origin
    for k, v in data.items():
        if not isinstance(k, str) or not isinstance(v, str):
            continue
        result = result.replace(k, v)
    return result


def _render_domain_files(template, template_file: str, domains: tuple):
    for domain in domains:
        data = _render_data(template.data, domain)
        domain_file = _replace_data(template_file, data)
        _copy_and_replace(template_file, domain_file, data)


def _copy_and_replace(src: str, dst: str, data: dict):
    dst_dir, _ = os.path.split(dst)
    os.makedirs(dst_dir, exist_ok=True)
    with open(src, "r", encoding="utf-8") as read:
        with open(dst, "w", encoding="utf-8") as write:
            for line in read:
                new_line = _replace_data(line, data)
                new_line = _replace_if_prop_exist(new_line, data["${language.code}"], data["properties"])
                write.write(new_line)
                write.flush()
            write.close()
        read.close()


def _replace_if_prop_exist(line: str, language_code: str, properties: list):
    if "${property.type}" not in line or properties is None:
        return line
    result = ""
    type_map = dict_type_by_lang_code(language_code)
    for prop in properties:
        result += "\n"
        result += line.replace("${property.type}", type_map[prop.type]).replace("${property.name}", prop.name)
    return result
