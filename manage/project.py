import os

from git import Repo

from plugin import delete_dir
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
            template_path = os.path.join(project_dir, template.path)
            template_dir, template_file = os.path.split(template_path)
            for domain in domains:
                data = _render_data(template.data, domain)
                domain_file = _replace_data(template_file, data)
                _copy_and_replace(template_path, os.path.join(template_dir, domain_file), data)

    def __find_project_domains_templates(self, param):
        domain = self.__domain_service.find_by_code(param.domain_code)
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
    return data

def _replace_data(origin: str, data: dict):
    result = origin
    for k, v in data.items():
        result = result.replace(k, v)
    return result

def _copy_and_replace(src: str, dst: str, map: dict):
    with open(src, "r", encoding="utf-8") as read:
        with open(dst, "w", encoding="utf-8") as write:
            for line in read:
                write.write(_replace_data(line, map))
                write.flush()
            write.close()
        read.close()
