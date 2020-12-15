import os


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
