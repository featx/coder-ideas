import os

from git import Repo, Actor

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


def _git_repo_push(repo: Repo, repo_url: str, branch: str, api_token: str):
    # check current branch is the project configured branch
    if repo.active_branch.name != branch:
        repo.head.reference = repo.create_head(branch)
        assert not repo.head.is_detached
        repo.head.reset(index=True, working_tree=True)
    # check repo url is configured.  No remote to push
    if repo_url is None or repo_url.strip() == "":
        return
    url = repo_url
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
