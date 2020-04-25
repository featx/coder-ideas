from context.exception import BusinessError
from service.data_engine import DataEngineService
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

    def create_project_data_engine(self, data_engine):
        project = self.__project_service.find_by_code(data_engine.project_code)
        if project is None:
            raise BusinessError.PROJECT_NOT_FOUND.value.and_with(data_engine.project_code)
        project_data_engine = self.__project_data_engine_service.create(_to_project_data_engine(data_engine))
        return project_data_engine


def _to_project_data_engine(data_engine):
    return ProjectDateEngine(
        code=data_engine.code,
        data_engine_code=data_engine.data_engine_code,
        project_code=data_engine.project_code,
        comment=data_engine.comment
    )
