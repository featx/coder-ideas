from aiohttp import web
from aiohttp.web_request import Request

from handler import json_exception, ModelFromDict
from manage.template import TemplateManager


class TemplateHandler:
    def __init__(self, managers):
        self.__template_manager: TemplateManager = managers["template"]

    def routes(self):
        return [
            web.post('/template', self.post),
            web.put('/template', self.put),
            web.delete('/template', self.delete),
            # Read ones
            web.get('/template', self.get),
            web.get('/templates', self.list_all),
            web.get('/template/detail', self.detail),
            web.get('/template/page', self.page)
        ]


    @json_exception
    async def post(self, request: Request):
        body = await request.json()
        template = self.__template_manager.create(CreatingTemplate(body))
        return {"id": template.id, "code": template.code}

    @json_exception
    async def put(self, request: Request):
        body = await request.json()
        template = self.__template_manager.update(UpdatingTemplate(body))
        return {"id": template.id, "code": template.code}

    @json_exception
    async def delete(self, request: Request):
        code = request.query.get("code")
        self.__template_manager.delete(code)
        return True

    @json_exception
    async def get(self, request: Request):
        code = request.query.get("code")
        return self.__template_manager.get(code)

    @json_exception
    async def list_all(self, request: Request):
        return self.__template_manager.list_all()

    @json_exception
    async def detail(self, request: Request):
        return web.json_response({"code": -1, "result": "not implemented"})

    @json_exception
    async def page(self, request: Request):
        body = await request.json()
        return self.__template_manager.page(body)


class CreatingTemplate(ModelFromDict):
    type = 0
    sort = 0
    language_code = ""
    framework_code = ""

class UpdatingTemplate(ModelFromDict):
    repo_url = None
    name = None
    type = None
    sort = None
    language_code = None
    framework_code = None
    api_token = None
    branch = None
