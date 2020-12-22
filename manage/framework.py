from service.framework import FrameworkService
from service.model.framework import Framework


class FrameworkManager:

    def __init__(self, services):
        self.__framework_service: FrameworkService = services["framework"]

    def list_all(self):
        result = []
        frameworks = self.__framework_service.list_all()
        for framework in frameworks:
            result.append(_from_framework(framework))
        return result


def _from_framework(framework: Framework):
    return {
        "id": framework.id,
        "code": framework.code,
        "name": framework.name
    }