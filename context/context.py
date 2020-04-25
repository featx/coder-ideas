import os

import yaml
from aiohttp import web
from sqlalchemy.orm import sessionmaker

from context.data_source import create_session_factory
from handler.data_engine import DataEngineHandler
from handler.domain import DomainHandler
from handler.project import ProjectHandler
from handler.template import TemplateHandler
from manage.data_engine import DataEngineManager
from manage.domain import DomainManager
from manage.project import ProjectManager
from manage.template import TemplateManager
from service.data_engine import DataEngineService
from service.domain_property import DomainPropertyService
from service.project import ProjectService
from service.project_data_engine import ProjectDataEngineService
from service.project_domain import ProjectDomainService
from service.project_template import ProjectTemplateService


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
        session_maker = create_session_factory(self.context.config["data_source"]["mysql"])
        self.services(session_maker)
        self.managers()
        self.handlers()
        self.__http_server = web.Application()
        for handler in self.context.handlers:
            self.__http_server.add_routes(handler.routes())

    def __delete__(self, instance):
        self.__http_server.cleanup()

    def start(self):
        web.run_app(self.__http_server)

    def services(self, session_maker: sessionmaker):
        self.context.services["data-engine"] = DataEngineService(session_maker)

        self.context.services["project"] = ProjectService(session_maker)
        self.context.services["project-template"] = ProjectTemplateService(session_maker)
        self.context.services["project-domain"] = ProjectDomainService(session_maker)
        self.context.services["domain-property"] = DomainPropertyService(session_maker)
        self.context.services["project-data-engine"] = ProjectDataEngineService(session_maker)

    def managers(self):
        git_workspace = self.context.config["version_control"]["git"]["work_path"]
        self.context.managers["project"] = ProjectManager(self.context.services, git_workspace)
        self.context.managers["template"] = TemplateManager(self.context.services)
        self.context.managers["domain"] = DomainManager(self.context.services)
        self.context.managers["data-engine"] = DataEngineManager(self.context.services)

    def handlers(self):
        self.context.handlers.append(ProjectHandler(self.context.managers))
        self.context.handlers.append(TemplateHandler(self.context.managers))
        self.context.handlers.append(DomainHandler(self.context.managers))
        self.context.handlers.append(DataEngineHandler(self.context.managers))
