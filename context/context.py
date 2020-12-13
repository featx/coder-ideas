import os

import yaml
from aiohttp import web
from sqlalchemy.orm import sessionmaker

from context.data_source import create_session_factory
from handler.data_engine import DataEngineHandler
from handler.domain import DomainHandler
from handler.framework import FrameworkHandler
from handler.language import LanguageHandler
from handler.project import ProjectHandler
from handler.template import TemplateHandler
from manage.data_engine import DataEngineManager
from manage.domain import DomainManager
from manage.framework import FrameworkManager
from manage.language import LanguageManager
from manage.project import ProjectManager
from manage.template import TemplateManager
from service.data_engine import DataEngineService
from service.domain_property import DomainPropertyService
from service.framework import FrameworkService
from service.language import LanguageService
from service.project import ProjectService
from service.project_data_engine import ProjectDataEngineService
from service.project_domain import ProjectDomainService
from service.template import TemplateService
from service.template_entry import TemplateEntryService


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
        web.run_app(self.__http_server, port=8081)

    def services(self, session_maker: sessionmaker):
        self.context.services["data-engine"] = DataEngineService(session_maker)
        self.context.services["language"] = LanguageService(session_maker)
        self.context.services["framework"] = FrameworkService(session_maker)

        self.context.services["template"] = TemplateService(session_maker)
        self.context.services["template-entry"] = TemplateEntryService(session_maker)

        self.context.services["project"] = ProjectService(session_maker)
        self.context.services["project-data-engine"] = ProjectDataEngineService(session_maker)
        self.context.services["project-domain"] = ProjectDomainService(session_maker)
        self.context.services["domain-property"] = DomainPropertyService(session_maker)

    def managers(self):
        self.context.managers["data-engine"] = DataEngineManager(self.context.services)
        self.context.managers["language"] = LanguageManager(self.context.services)
        self.context.managers["framework"] = FrameworkManager(self.context.services)

        git_templates = self.context.config["version_control"]["git"]["templates"]
        git_workspace = self.context.config["version_control"]["git"]["workspace"]
        self.context.managers["template"] = TemplateManager(self.context.services, git_templates)
        self.context.managers["project"] = ProjectManager(self.context.services, git_workspace)

        self.context.managers["domain"] = DomainManager(self.context.services)

    def handlers(self):
        self.context.handlers.append(DataEngineHandler(self.context.managers))
        self.context.handlers.append(LanguageHandler(self.context.managers))
        self.context.handlers.append(FrameworkHandler(self.context.managers))

        self.context.handlers.append(TemplateHandler(self.context.managers))

        self.context.handlers.append(ProjectHandler(self.context.managers))
        self.context.handlers.append(DomainHandler(self.context.managers))
