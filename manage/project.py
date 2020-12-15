import os
import shutil

from git import Repo
from git import Actor

from context.exception import BusinessError
from manage import _repo_dir
from manage.domain import _from_project_domain
from plugin.language_type import dict_type_by_lang_code
from service.project_domain import ProjectDomainService
from service.model.project import Project, ProjectPageCriteria
from service.project import ProjectService
from service.template import TemplateService


class ProjectManager:
    def __init__(self, services, templates: str, workspace: str):
        self.__project_service: ProjectService = services["project"]
        self.__template_service: TemplateService = services["template"]
        self.__domain_service: ProjectDomainService = services["project-domain"]
        self.__git_workspace = workspace
        self.__git_templates = templates

    def create(self, creating_project):
        if creating_project.template_code is None or creating_project.template_code.strip() == "":
            raise BusinessError.PARAMETER_LOST
        template = self.__template_service.find_by_code(creating_project.template_code)
        if template is None:
            raise BusinessError.TEMPLATE_NOT_FOUND
        template_dir = _repo_dir(self.__git_templates, template.repo_url)
        # TODO May be require lock repo
        template_repo = Repo.init(template_dir)
        files = []
        for entry in template_repo.index.entries:
            files.append(entry[0])
        template_repo.close()

        project = self.__project_service.create(_to_project(creating_project))
        project_dir = os.path.join(self.__git_workspace, project.code)
        shutil.copytree(template_dir, project_dir)
        shutil.rmtree(project_dir + os.path.sep + ".git")

        project_repo = Repo.init(project_dir)
        project_repo.index.add(files)
        if project.repo_url is not None and project.repo_url.strip() != "":
            project_repo.create_remote('origin', project.repo_url)
        project_repo.close()

        return project

    def update(self, param):
        if param.project_code is None or param.project_code.strip() != "":
            return
        project = self.__project_service.find_by_code(param.project_code)

    def delete(self, project_code):
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
        project, domains, templates = self.__find_project_domains_templates(param)
        if project is None:
            return
        project_dir = os.path.join(self.__git_workspace, project.code)
        
        files_to_add = []
        files_to_remove = []
        for template in templates:
            template.data["${language.code}"] = project.language_code
            template_path = os.path.join(project_dir, template.path)
            if os.path.isfile(template_path):
                template_file = template_path
                files_to_remove.append(template.path)
                files_to_add += _render_domain_files(template, template_file, domains)
            elif os.path.isdir(template_path):
                for _file in os.listdir(template_path):
                    template_file = os.path.join(template_path, _file)
                    files_to_remove.append(os.path.join(template.path, _file))
                    files_to_add += _render_domain_files(template, template_file, domains)
        if len(files_to_add) > 0:
            repo = Repo(project_dir)
            repo.index.add(files_to_add)
            _git_repo_remove(files_to_remove, repo)

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

    def commit_push(self, param):
        if param.project_code is None or param.project_code.strip() == "":
            return 
        project = self.__project_service.find_by_code(param.project_code)
        project_dir = os.path.join(self.__git_workspace, project.code)
        repo = Repo(project_dir)
        
        try:
            repo.commit("HEAD")
        except Exception:
            # TODO While permission component change the hard code to variables
            actor = Actor("之外", "excepts@featx.org")
            repo.index.commit("Init", author=actor, committer=actor)

        _git_repo_push(repo, project)


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
        "repo_url": project.repo_url,
        "branch": project.branch,
        "comment": project.comment
    }


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
    domain_files = []
    for domain in domains:
        data = _render_data(template.data, domain)
        domain_file = _replace_data(template_file, data)
        _copy_and_replace(template_file, domain_file, data)
        domain_files.append(domain_file)
    return domain_files


def _copy_and_replace(src: str, dst: str, data: dict):
    dst_dir, _ = os.path.split(dst)
    os.makedirs(dst_dir, exist_ok=True)
    try:
        read = open(src, "r", encoding="utf-8")
        write = open(dst, "w", encoding="utf-8")
        for line in read:
            new_line = _replace_data(line, data)
            if "properties" in data:
                properties = data["properties"]
            else:
                properties = None
            new_line = _replace_if_prop_exist(new_line, data["${language.code}"], properties)
            write.write(new_line)
            write.flush()
    except Exception as e:
        pass
    finally:
        if write is not None:
            write.close()
        if read is not None:
            read.close()


def _replace_if_prop_exist(line: str, language_code: str, properties: list):
    if "${property.type}" not in line or properties is None:
        return line
    result = ""
    type_map = dict_type_by_lang_code(language_code)
    for prop in properties:
        result += line.replace("${property.type}", type_map[prop.type]).replace("${property.name}", prop.name)
        result += "\n"
    return result


def _git_repo_remove(files_to_remove: list, repo: Repo):
    files_remove = files_to_remove.copy()
    for remove_file in files_to_remove:
        require_drop = False
        for entry in repo.index.entries:
            if entry[0] == remove_file:
                require_drop = True
                break
        if not require_drop:
            files_remove.remove(remove_file)
    if len(files_remove) > 0:
        repo.index.remove(files_remove)


def _git_repo_push(repo: Repo, project: Project):
    # check current branch is the project configured branch 
    if repo.active_branch.name != project.branch:
        repo.head.reference = repo.create_head(project.branch)
        assert not repo.head.is_detached
        repo.head.reset(index=True, working_tree=True)
    # check repo url is configured.  No remote to push
    if project.repo_url is None or project.repo_url.strip() == "":
        return
    url = project.repo_url
    # if api token configured, set it.
    if project.api_token is not None and project.api_token.strip() != "":
        url = url.replace("https://", "https://%s@" % (project.api_token))\
                .replace("http://", "http://%s@" % (project.api_token))
    # check if origin remote existed
    if 'origin' not in repo.remotes:
        repo.create_remote('origin', url)
    else:
        origin = repo.remotes.origin
        origin.set_url(url)
    # check remote branch existed    
    if project.branch in repo.remotes['origin'].refs:
        repo.remotes.origin.push()
    else:
        repo.git.push('--set-upstream', 'origin', project.branch)
