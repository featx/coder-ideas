from sqlalchemy.orm import sessionmaker, scoped_session

from plugin import IdGenerate
from plugin.snowflake import SnowFlake

from service import transactional
from service.model.project import Project


class ProjectService:

    def __init__(self, session_maker: sessionmaker):
        self.__id_generator: IdGenerate = SnowFlake()
        self.__session_maker = session_maker
        self._scoped_session = scoped_session(session_maker)

    @transactional
    def create(self, project: Project):
        session = self._scoped_session()
        if project.code is None or project.code.strip() == "":
            project.code = "PJT{}".format(self.__id_generator.next_base_36())
        session.add(project)
        return project

    def find_by_code(self, project_code: str):
        if project_code is None or project_code.strip() == "":
            return None
        session = self._scoped_session()
        return session.query(Project).filter_by(code=project_code).first()

    @transactional
    def delete(self, project_code):
        session = self._scoped_session()
        project = session.query(Project).filter_by(code=project_code).first()
        if project is None:
            raise Exception
        project.deleted = True
        return True
