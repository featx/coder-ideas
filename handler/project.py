from aiohttp import web
from aiohttp.web_request import Request

from model.project import Project
from service.project import ProjectService


class ProjectHandler:
    def __init__(self, services):
        self.__project_service: ProjectService = services["project"]

    def routes(self):
        return [web.post('/project', self.create),
                web.delete('/project', self.delete),
                web.get('/project', self.get)]

    async def create(self, request: Request):
        body = await request.json()
        code = self.__project_service.create(Project(
            code=body['code'],
            name=body['name'],
            template_repo_url=body['template_repo_url'],
            template_api_token=body['template_api_token'],
            repo_url=body['repo_url'],
            api_token=body['api_token']
        ))
        return web.json_response({"code": 0, "result": code})

    async def update(self, request):
        return web.json_response({"code": -1, "result": "not implemented"})

    async def delete(self, request):
        return web.json_response({"code": -1, "result": "not implemented"})

    async def get(self, request):
        return web.json_response({"code": -1, "result": "not implemented"})