from sqlalchemy.orm import scoped_session, sessionmaker

from model.project import Project


class ProjectService:

    def __init__(self, session_maker: sessionmaker):
        self.__session_maker = session_maker

    def create(self, project: Project):
        session = scoped_session(self.__session_maker)
        session.add(project)
        session.commit()
