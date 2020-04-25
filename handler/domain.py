from aiohttp import web
from aiohttp.web_request import Request

from handler import ModelFromDict, json_exception
from manage.domain import DomainManager
from manage.project import ProjectManager


class DomainHandler:
    def __init__(self, managers):
        self.__project_manager: ProjectManager = managers["project"]
        self.__domain_manager: DomainManager = managers["domain"]

    def routes(self):
        return [web.post('/domain', self.create),
                web.delete('/domain', self.delete),
                web.get('/domain', self.get),
                web.post('/project/domain', self.create_for_project),
                web.delete('/project/domain', self.delete_of_project),
                web.get('/project/domain', self.get_of_project)]

    @json_exception
    async def create(self, request: Request):
        body = await request.json()
        project = self.__project_manager.create(ModelFromDict(body))
        return {"id": project.id, "code": project.code}

    async def update(self, request):
        return web.json_response({"code": -1, "result": "not implemented"})

    async def delete(self, request):
        return web.json_response({"code": -1, "result": "not implemented"})

    async def get(self, request):
        return web.json_response({"code": -1, "result": "not implemented"})

    async def page(self, request):
        return web.json_response({"code": -1, "result": "not implemented"})

    @json_exception
    async def create_for_project(self, request: Request):
        body = await request.json()
        project = self.__domain_manager.create(ModelFromDict(body))
        return {"id": project.id, "code": project.code}

    async def update(self, request):
        return web.json_response({"code": -1, "result": "not implemented"})

    async def delete_of_project(self, request):
        return web.json_response({"code": -1, "result": "not implemented"})

    async def get_of_project(self, request):
        return web.json_response({"code": -1, "result": "not implemented"})