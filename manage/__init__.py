import codecs
import os
import shutil

from git import Repo, Actor

from plugin.language_type import dict_type_by_lang_code
from plugin.string_util import snake, camel, kebab
from service.model.project import Project
from service.model.project_domain import ProjectDomain

RULE_MARK = ".rul"
BRANCH_CODER = "coder"
FEATX_CODER = Actor("Coder", "coder@featx.org")


_TEXT_BOMS = (
    codecs.BOM_UTF16_BE,
    codecs.BOM_UTF16_LE,
    codecs.BOM_UTF32_BE,
    codecs.BOM_UTF32_LE,
    codecs.BOM_UTF8,
    )


def _repo_dir(template_path: str, url: str):
    left = url.index(":") + 1
    if left < 0:
        left = 0
    right = len(url)
    if url.endswith(".git"):
        right = right - 4
    paths = url[left:right]
    while paths.startswith('/'):
        paths = paths[1:]
    result = os.path.join(template_path, paths)
    return result


def _repo_with_token_url(url: str, api_token: str):
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


def _replace_data(origin: str, data: dict):
    result = origin
    for k, v in data.items():
        if not isinstance(k, str) or not isinstance(v, str):
            continue
        result = result.replace(k, v)
    return result


def _copy_and_replace(src: str, dst: str, data: dict):
    language_code = None
    if data.__contains__("${language.code}"):
        language_code = data["${language.code}"]
    if "properties" in data:
        properties = data["properties"]
    else:
        properties = None

    dst_dir, _ = os.path.split(dst)
    os.makedirs(dst_dir, exist_ok=True)
    read, write = None, None
    try:
        if is_binary_file(src):
            read = open(src, "rb")
            write = open(dst, "wb")
            for line in read:
                write.write(line)
        else:
            read = open(src, "r", encoding="utf-8")
            write = open(dst, "w", encoding="utf-8")
            for line in read:
                new_line = _replace_data(line, data)
                new_line = _replace_if_prop_exist(new_line, language_code, properties)
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


def _git_repo_push(repo: Repo, remote_url: str, branch: str, api_token: str):
    # check current branch is the project configured branch
    if repo.active_branch.name != branch:
        repo.head.reference = repo.create_head(branch)
        assert not repo.head.is_detached
        repo.head.reset(index=True, working_tree=True)
    # check repo url is configured.  No remote to push
    if remote_url is None or remote_url.strip() == "":
        return
    url = remote_url
    # if api token configured, set it.
    if api_token is not None and api_token.strip() != "":
        url = url.replace("https://", "https://%s@" % api_token)\
                .replace("http://", "http://%s@" % api_token)
    # check if origin remote existed
    if 'origin' not in repo.remotes:
        repo.create_remote('origin', url)
    else:
        origin = repo.remotes.origin
        origin.set_url(url)
    # check remote branch existed
    if branch in repo.remotes['origin'].refs:
        repo.remotes.origin.push()
    else:
        repo.git.push('--set-upstream', 'origin', branch)


def is_binary_file(file_path):
    with open(file_path, 'rb') as file:
        initial_bytes = file.read(8192)
        file.close()
        for bom in _TEXT_BOMS:
            if initial_bytes.startswith(bom):
                continue
            else:
                if b'\0' in initial_bytes:
                    return True
    return False


# Git Repo Serial
def repo_clone_checkout(repo_url, api_token, local_dir, checkout_to):
    repo_url = _repo_with_token_url(repo_url, api_token)
    result = ""
    try:
        if not os.path.exists(local_dir):
            os.makedirs(local_dir, 755)
            # TODO It's required to remove dir, while clone exception.
            repo = Repo.clone_from(repo_url, local_dir, branch=checkout_to)
        else:
            repo = Repo.init(local_dir)  # Checkout the branch
            repo.git.repo_checkout(checkout_to)
        result = repo.head.commit.hexsha
        repo.close()
    except Exception as e:
        # logging.INFO("Clone or check out error")
        os.remove(local_dir)
    return result


def repo_checkout(local_dir: str, checkout_to: str):
    repo = Repo.init(local_dir)
    repo.git.repo_checkout(checkout_to)
    repo.git.pull()
    result = repo.head.commit.hexsha
    repo.close()
    return result


def repo_copy(from_dir: str, to_dir: str, replaces: dict):
    try:
        from_repo = Repo.init(from_dir)
        files = []
        for file, ind in from_repo.index.entries:
            if not file.endswith(RULE_MARK):
                new_file = _replace_data(file, replaces)
                _copy_and_replace(os.path.join(from_dir, file), os.path.join(to_dir, new_file), replaces)
                files.append(new_file)
        from_repo.close()

        to_repo = Repo.init(to_dir)
        to_repo.index.add(files)
        to_repo.index.commit("Init", author=FEATX_CODER, committer=FEATX_CODER)
        to_repo.close()
        return
    except Exception as e:
        return


def repo_add(repo_dir: str, files: [str]):
    try:
        repo = Repo(repo_dir)
        repo.index.add(files)
    except Exception as e:
        pass


def repo_commit(local_dir: str):
    repo = None
    try:
        repo = Repo(local_dir)
        repo.index.commit("Init", author=FEATX_CODER, committer=FEATX_CODER)
    except Exception:
        pass
    finally:
        if repo is not None:
            repo.close()


def repo_push(local_repo: str, remote_url: str, branch: str, api_token: str):
    repo = None
    try:
        repo = Repo(local_repo)
        _git_repo_push(repo, remote_url, branch, api_token)
    except Exception as e:
        pass
    finally:
        if repo is not None:
            repo.close()


def repo_commit_push(local_dir: str, remote_url: str, branch: str, api_token: str):
    repo = None
    try:
        repo = Repo(local_dir)
        repo.index.commit("Init", author=FEATX_CODER, committer=FEATX_CODER)
        _git_repo_push(repo, remote_url, branch, api_token)
    except Exception as e:
        pass
    finally:
        if repo is not None:
            repo.close()


# Files Ops
def delete_dir(local_dir: str):
    shutil.rmtree(local_dir)


# Object converters
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


def _from_project_domain(project_domain):
    properties = []
    for prop in project_domain.properties:
        properties.append(_from_domain_property(prop))
    return {
        "code": project_domain.code,
        "name": project_domain.name,
        "type": project_domain.type,
        "project_code": project_domain.project_code,
        "comment": project_domain.comment,
        "properties": properties
    }


def _from_domain_property(domain_property):
    return {
        "id": domain_property.id,
        "code": domain_property.code,
        "name": domain_property.name,
        "type": domain_property.type,
        "sort": domain_property.sort,
        "domain_code": domain_property.domain_code,
        "project_code": domain_property.project_code
    }


# Render data
def _render_project(template: dict, project: Project):
    data = dict()
    for key, value in template.items():
        k = key.replace("${project.name|lower}", project.name.lower())
        k = k.replace("${project.name}", project.name)
        v = value.replace("${project.name|lower}", project.name.lower())
        v = v.replace("${project.name}", project.name)
        if project.variables['packageRoot']:
            package_root = project.variables['packageRoot']
            k = k.replace("${project.packageRoot}", package_root)
            k = k.replace("${project.packageRoot|path}", package_root.replace('.', os.path.sep))
            k = k.replace("${project.packageRoot|dot}", package_root)
            v = v.replace("${project.packageRoot}", package_root)
            v = v.replace("${project.packageRoot|path}", package_root.replace('.', os.path.sep))
            v = v.replace("${project.packageRoot|dot}", package_root)
        data[k] = v
    return data


def _render_domain(template: dict, domain: ProjectDomain):
    data = dict()
    for key, value in template.items():
        k = key.replace("${domain.name|camel}", camel(domain.name))
        k = k.replace("${domain.name|lowerCamel}", camel(domain.name, True))
        k = k.replace("${domain.name|snake}", snake(domain.name))
        k = k.replace("${domain.name|dash}", kebab(domain.name))
        v = value.replace("${domain.name|camel}", camel(domain.name))
        v = v.replace("${domain.name|lowerCamel}", camel(domain.name, True))
        v = v.replace("${domain.name|snake}", snake(domain.name))
        v = v.replace("${domain.name|dash}", kebab(domain.name))
        data[k] = v
    if hasattr(domain, "properties"):
        data["properties"] = domain.properties
    return data


def _render_domain_files(rule_path: str, domain_path: str, data, domains: list):
    domain_files = []
    for domain in domains:
        data = _render_domain(data, domain)
        domain_file = _replace_data(domain_path, data)
        if domain_file.endswith(RULE_MARK):
            domain_file = domain_file[:-4]
        # rule has type 1 and domain contains properties
        data["properties"] = domain.properties
        _copy_and_replace(rule_path, domain_file, data)
        domain_files.append(domain_file)
    return domain_files
