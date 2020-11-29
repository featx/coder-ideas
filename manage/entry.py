from context.exception import BusinessError
from service.project import ProjectService
from service.template import TemplateService


class TemplateManager:
    def __init__(self, services):
        self.__project_service: ProjectService = services["project"]
        self.__template_service: TemplateService = services["template"]

    def create(self, creating_template):
        project = self.__project_service.find_by_code(creating_template.project_code)
        if project is None:
            raise BusinessError.PROJECT_NOT_FOUND.value.and_with(creating_template.project_code)
        project_template = self.__template_service.create(_to_project_template(creating_template))
        return project_template


def _to_project_template(creating_template):
    return ProjectTemplate(
        code=creating_template.code,
        name=creating_template.name,
        project_code=creating_template.project_code,
        path=creating_template.path,
        engine=creating_template.engine,
        data=creating_template.data,
        comment=creating_template.comment
    )


def _from_template_entry(project_template):
    return {
        "code": project_template.code,
        "name": project_template.name,
        "project_code": project_template.project_code,
        "path": project_template.path,
        "engine": project_template.engine,
        "data": project_template.data,
        "comment": project_template.comment
    }