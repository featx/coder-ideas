import os

from git import Repo

from plugin import delete_dir
from service.model.project import Project
from service.project import ProjectService


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
        self.__git_workspace = workspace

    def create(self, creating_project):
        repo_dir = os.path.join(self.__git_workspace, creating_project.name)

        # Clone from template project
        url = _repo_with_token_url(creating_project.template_repo_url, creating_project.template_api_token)
        repo = Repo.clone_from(url, repo_dir, branch=creating_project.template_branch)
        creating_project.template_commit = repo.head.commit.hexsha
        repo.close()
        delete_dir(os.path.join(repo_dir, ".git"))

        project = self.__project_service.create(self.__to_project(creating_project))

        project_dir = os.path.join(self.__git_workspace, project.code)
        os.rename(repo_dir, project_dir)
        Repo.init(project_dir).close()
        return project

    def __to_project(self, creating_project):
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
