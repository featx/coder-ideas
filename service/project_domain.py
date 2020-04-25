from sqlalchemy.orm import sessionmaker, scoped_session

from plugin import IdGenerate
from plugin.snowflake import SnowFlake
from service import transactional
from service.model.project_domain import ProjectDomain


class ProjectDomainService:

    def __init__(self, session_maker: sessionmaker):
        self.__id_generator: IdGenerate = SnowFlake()
        self.__session_maker = session_maker
        self._scoped_session = scoped_session(session_maker)

    def find_by_project_code(self, project_code):
        session = self._scoped_session()
        return session.query(ProjectDomain).filter_by(project_code=project_code).all()

    @transactional
    def create(self, project_domain: ProjectDomain):
        session = self._scoped_session()
        if project_domain.code is None or project_domain.code.strip() == "":
            project_domain.code = "PDM{}".format(self.__id_generator.next_base_36())
        session.add(project_domain)
        return project_domain
