from sqlalchemy.orm import sessionmaker, scoped_session

from service import transactional
from service.model.project import Project


class ProjectService:

    def __init__(self, session_maker: sessionmaker):
        self.__session_maker = session_maker
        self.__scoped_session = scoped_session(session_maker)

    @transactional
    def create(self, project: Project):
        session = self.__scoped_session()
        session.add(project)
        return project
