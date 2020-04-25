from sqlalchemy.orm import sessionmaker, scoped_session

from plugin import IdGenerate
from plugin.snowflake import SnowFlake
from service import transactional
from service.model.domain_property import DomainProperty


class DomainPropertyService:

    def __init__(self, session_maker: sessionmaker):
        self.__id_generator: IdGenerate = SnowFlake()
        self.__session_maker = session_maker
        self._scoped_session = scoped_session(session_maker)

    def find_by_project_code(self, project_code):
        session = self._scoped_session()
        return session.query(DomainProperty) \
            .filter_by(project_code=project_code).all()

    @transactional
    def create(self, domain_property: DomainProperty):
        session = self._scoped_session()
        if domain_property.code is None or domain_property.code.strip() == "":
            domain_property.code = "DMP{}".format(self.__id_generator.next_base_36())
        session.add(domain_property)
        return domain_property
