from aiohttp import web
from aiohttp.web_request import Request

from handler import ModelFromDict, json_exception
from manage.project import ProjectManager


class ProjectHandler:
    def __init__(self, managers):
        self.__project_manager: ProjectManager = managers["project"]

    def routes(self):
        return [web.post('/project', self.create),
                web.put('/project', self.update),
                web.delete('/project', self.delete),
                web.get('/project', self.get),
                web.get('/project/detail', self.detail),
                web.get('/project/page', self.page),
                web.post('/project/generate', self.generate),
                web.post('/project/commit', self.commit_push)
                ]

    @json_exception
    async def create(self, request: Request):
        body = await request.json()
        project = self.__project_manager.create(CreatingProject(body))
        return {"id": project.id, "code": project.code}

    @json_exception
    async def update(self, request: Request):
        body = await request.json()
        project = self.__project_manager.update(ModelFromDict(body))
        return {"id": project.id, "code": project.code}

    @json_exception
    async def delete(self, request: Request):
        project_code = request.query.get("code")
        self.__project_manager.delete(project_code)
        return True

    @json_exception
    async def get(self, request: Request):
        project_code = request.query.get("code")
        return self.__project_manager.get(project_code)

    @json_exception
    async def detail(self, request: Request):
        project_code = request.query.get("code")
        return self.__project_manager.detail(project_code)

    @json_exception
    async def page(self, request: Request):
        body = await request.json()
        return self.__project_manager.page(body)

    @json_exception
    async def generate(self, request: Request):
        body = await request.json()
        self.__project_manager.generate(GenerateProject(body))
#TODO
        return True

    @json_exception
    async def commit_push(self, request: Request):
        body = await request.json()
        self.__project_manager.commit_push(ModelFromDict(body))


class CreatingProject(ModelFromDict):
    type = 0
    sort = 0
    template_code = None


class GenerateProject(ModelFromDict):
    domain_code = None
    rule_code = None
