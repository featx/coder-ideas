
from sqlalchemy.orm import sessionmaker, scoped_session

from plugin import IdGenerate
from plugin.snowflake import SnowFlake
from service import transactional
from service.model.data_engine import DataEngine


class DataEngineService:

    def __init__(self, session_maker: sessionmaker):
        self.__id_generator: IdGenerate = SnowFlake()
        self.__session_maker = session_maker
        self._scoped_session = scoped_session(session_maker)

    @transactional
    def create(self, data_engine: DataEngine):
        session = self._scoped_session()
        if data_engine.code is None or data_engine.code.strip() == "":
            data_engine.code = "DTE{}".format(self.__id_generator.next_base_36())
        session.add(data_engine)
        return data_engine

    def find_by_code(self, project_code):
        pass

