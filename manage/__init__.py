import os
import shutil

from git import Repo, Actor

from plugin.language_type import dict_type_by_lang_code

RULE_MARK = ".rul"
BRANCH_CODER = "coder"
FEATX_CODER = Actor("Coder", "coder@featx.org")


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
    dst_dir, _ = os.path.split(dst)
    os.makedirs(dst_dir, exist_ok=True)
    read, write = None, None
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


def snake_camel(camel: str):
    up_index = []
    for i, c in enumerate(camel):
        if c.isupper():
            up_index.append(i)
    ls = camel.lower()
    list_ls = list(ls)
    if up_index:
        addi = 0
        for g in up_index:
            list_ls.insert(g + addi, '_')
            addi += 1
    last_ls = ''.join(list_ls)
    return last_ls


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


def repo_copy(from_dir: str, to_dir: str, replaces):
    try:
        from_repo = Repo.init(from_dir)
        files = []
        for file, ind in from_repo.index.entries:
            if not file.endswith(RULE_MARK):
                files.append(file)
        from_repo.close()

        shutil.copytree(from_dir, to_dir)
        shutil.rmtree(to_dir + os.path.sep + ".git")

        to_repo = Repo.init(to_dir)
        to_repo.index.add(files)
        to_repo.index.commit("Init", author=FEATX_CODER, committer=FEATX_CODER)
        to_repo.close()
        return
    except Exception as e:
        return


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


def delete_dir(local_dir: str):
    shutil.rmtree(local_dir)
