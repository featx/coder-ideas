import os

from git import Repo

from service.model.template import Template, TemplatePageCriteria
from service.template import TemplateService


class TemplateManager:
    def __init__(self, services, templates: str):
        self.__template_service: TemplateService = services["template"]
        self.__git_templates = templates

    def _repo_dir(self, url: str):
        l = url.index(":") + 1
        if l < 0:
            l = 0
        r = len(url)
        if url.endswith(".git"):
            r = r - 4
        paths = url[l:r]
        while paths.startswith('/'):
            paths = paths[1:]
        result = os.path.join(self.__git_templates, paths)
        return result

    def create(self, creating_template):
        local_dir = self._repo_dir(creating_template.repo_url)
        # Clone from template project
        repo_url = _repo_with_token_url(creating_template.repo_url, creating_template.api_token)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir, 755)
            repo = Repo.clone_from(repo_url, local_dir, branch=creating_template.branch)
        else:
            repo = Repo.init(local_dir) # Checkout the branch
            # repo.git.checkout(creating_template.branch)
        creating_template.commit = repo.head.commit.hexsha
        repo.close()
        return self.__template_service.create(_to_template(creating_template))

    def delete(self, code):
        self.__template_service.delete(code)

    def get(self, template_code):
        project = self.__template_service.find_by_code(template_code)
        return _from_template(project)

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
        "comment": template.comment
    }