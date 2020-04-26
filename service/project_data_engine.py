from sqlalchemy.orm import sessionmaker, scoped_session

from plugin import IdGenerate
from plugin.snowflake import SnowFlake
from service import transactional
from service.model.project_data_engine import ProjectDateEngine
from service.model.project_domain import ProjectDomain


class ProjectDataEngineService:

    def __init__(self, session_maker: sessionmaker):
        self.__id_generator: IdGenerate = SnowFlake()
        self.__session_maker = session_maker
        self._scoped_session = scoped_session(session_maker)

    def find_by_project_code(self, project_code):
        session = self._scoped_session()
        return session.query(ProjectDomain).filter_by(project_code=project_code).all()

    @transactional
    def create(self, project_data_engine):
        session = self._scoped_session()
        if project_data_engine.code is None or project_data_engine.code.strip() == "":
            project_data_engine.code = "PDE{}".format(self.__id_generator.next_base_36())
        last_data_engine = session.query(ProjectDateEngine) \
            .filter_by(project_code=project_data_engine.project_code) \
            .order_by(ProjectDateEngine.sort.desc()) \
            .first()
        if last_data_engine is None:
            project_data_engine.sort = 1
        else:
            project_data_engine.sort = last_data_engine.sort + 1
        session.add(project_data_engine)
        return project_data_engine
