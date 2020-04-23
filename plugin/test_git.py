import datetime
import os
import time

import pytest
from git import Repo


@pytest.mark.pytestto
class TestGit:
    @pytest.mark.asserttest
    def test_git_remote(self):
        a = datetime.datetime.fromtimestamp(time.time(), tz=datetime.tzinfo)
        repo = Repo(os.path.abspath('.'))
        result = repo.git.execute("git ls-remote {}".format("https://github.com/featx/docker-tree.git"))
        print(result)

        # empty_repo = Repo.init(os.path.join(os.path.abspath('.'), 'empty'))
        # remote = empty_repo.create_remote("origin", "http://www.baidu.com")
        # assert remote.exists()
