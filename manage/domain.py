from context.exception import BusinessError
from service.domain_property import DomainPropertyService
from service.model.domain_property import DomainProperty
from service.project_domain import ProjectDomainService
from service.model.project_domain import ProjectDomain
from service.project import ProjectService


class DomainManager:
    def __init__(self, services):
        self.__project_service: ProjectService = services["project"]
        self.__domain_service: ProjectDomainService = services["project-domain"]
        self.__domain_property_service: DomainPropertyService = services["domain-property"]

    def create(self, creating_domain):
        project = self.__project_service.find_by_code(creating_domain.project_code)
        if project is None:
            raise BusinessError.PROJECT_NOT_FOUND.value.and_with(creating_domain.project_code)
        domain = self.__domain_service.create(_to_project_domain(creating_domain))
        domain_properties = []
        for prop in creating_domain.properties:
            prop.domain_code = domain.code
            prop.project_code = creating_domain.project_code
            domain_properties.append(_to_domain_property(prop))
        self.__domain_property_service.create(domain_properties)
        return domain


def _to_project_domain(creating_domain):
    return ProjectDomain(
        code=creating_domain.code,
        name=creating_domain.name,
        project_code=creating_domain.project_code,
        comment=creating_domain.comment
    )


def _to_domain_property(domain_property):
    return DomainProperty(
        code=domain_property.code,
        name=domain_property.name,
        domain_code=domain_property.domain_code,
        project_code=domain_property.project_code,
        comment=domain_property.comment
    )
