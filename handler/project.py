from aiohttp import web
from aiohttp.web_request import Request

from handler import ModelFromDict, json_exception
from manage.project import ProjectManager


class ProjectHandler:
    def __init__(self, managers):
        self.__project_manager: ProjectManager = managers["project"]

    def routes(self):
        return [web.post('/project', self.create),
                web.delete('/project', self.delete),
                web.get('/project', self.get)]

    @json_exception
    async def create(self, request: Request):
        body = await request.json()
        project = self.__project_manager.create(ModelFromDict(body))
        return {"id": project.id, "code": project.code}

    async def update(self, request: Request):
        return web.json_response({"code": -1, "result": "not implemented"})

    async def delete(self, request: Request):
        return web.json_response({"code": -1, "result": "not implemented"})

    async def get(self, request: Request):
        return web.json_response({"code": -1, "result": "not implemented"})

    async def detail(self, request: Request):
        pass

    async def page(self, request: Request):
        return web.json_response({"code": -1, "result": "not implemented"})
