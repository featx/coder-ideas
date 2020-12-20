from context.exception import BusinessError
from service.data_engine import DataEngineService
from service.model.data_engine import DataEngine
from service.model.project_data_engine import ProjectDateEngine
from service.project import ProjectService
from service.project_data_engine import ProjectDataEngineService


class DataEngineManager:
    def __init__(self, services):
        self.__data_engine_service: DataEngineService = services["data-engine"]
        self.__project_service: ProjectService = services["project"]
        self.__project_data_engine_service: ProjectDataEngineService = services["project-data-engine"]

    def create(self, data_engine):
        pass

    def create_project_data_engine(self, creating_data_engine):
        if creating_data_engine.project_code is None or creating_data_engine.project_code.strip() == "":
            raise BusinessError.PARAMETER_LOST.with_info("project code")
        if creating_data_engine.data_engine_code is None or creating_data_engine.data_engine_code.strip() == "":
            raise BusinessError.PARAMETER_LOST.with_info("data engine code")
        project = self.__project_service.find_by_code(creating_data_engine.project_code)
        if project is None:
            raise BusinessError.PROJECT_NOT_FOUND.with_info(creating_data_engine.project_code)
        data_engine = self.__data_engine_service.find_by_code(creating_data_engine.data_engine_code)
        if data_engine is None:
            raise BusinessError.DATA_ENGINE_NOT_FOUND.with_info(creating_data_engine.data_engine_code)
        project_data_engine = self.__project_data_engine_service.create(_to_project_data_engine(creating_data_engine))
        return project_data_engine

    def list_all(self):
        result = []
        data_engines = self.__data_engine_service.list_all()
        for data_engine in data_engines:
            result.append(_from_data_engine(data_engine))
        return result


def _to_project_data_engine(data_engine):
    return ProjectDateEngine(
        code=data_engine.code,
        data_engine_code=data_engine.data_engine_code,
        project_code=data_engine.project_code,
        comment=data_engine.comment
    )

def _from_data_engine(data_engine: DataEngine):
    return {
        "id": data_engine.id,
        "code": data_engine.code,
        "name": data_engine.name
    }