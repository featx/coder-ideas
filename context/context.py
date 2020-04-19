import os

import yaml
from aiohttp import web

from context.data_source import create_session_factory
from handler.project import ProjectHandler
from manage.project import ProjectManager
from service.project import ProjectService


class CoderContext:
    config: None
    session_factory = None
    handlers = []
    managers = {}
    services = {}
    repositories = []

    def __init__(self):
        config_yml = open(os.path.abspath("./config/config.yml"), 'r', encoding="utf-8")
        config = config_yml.read()
        config_yml.close()
        self.config = yaml.load(config, Loader=yaml.FullLoader)


class CoderApplication:

    def __init__(self):
        self.context = CoderContext()
        self.context.session_factory = \
            create_session_factory(self.context.config["data_source"]["mysql"])

        self.services()
        self.managers()
        self.handlers()
        self.__http_server = web.Application()
        for handler in self.context.handlers:
            self.__http_server.add_routes(handler.routes())

    def __delete__(self, instance):
        self.__http_server.cleanup()

    def start(self):
        web.run_app(self.__http_server)

    def services(self):
        self.context.services["project"] = ProjectService(self.context.session_factory)

    def managers(self):
        git_workspace = self.context.config["version_control"]["git"]["work_path"]
        self.context.managers["project"] = ProjectManager(self.context.services, git_workspace)

    def handlers(self):
        self.context.handlers.append(ProjectHandler(self.context.managers))
