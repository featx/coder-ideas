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
    def create(self, domain_properties: tuple):
        session = self._scoped_session()
        last_property = session.query(DomainProperty) \
            .filter_by(domain_code=domain_properties[0].domain_code) \
            .order_by(DomainProperty.sort.desc()) \
            .first()
        start = 1
        if last_property is not None:
            start = last_property.sort + 1
        for domain_property in domain_properties:
            if domain_property.code is None or domain_property.code.strip() == "":
                domain_property.code = "DMP{}".format(self.__id_generator.next_base_36())
            domain_property.sort = start
            session.add(domain_property)
            start = start + 1
        return domain_properties
