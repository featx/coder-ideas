from aiohttp import web
from aiohttp.web_request import Request

from handler import json_exception, ModelFromDict
from manage.template import TemplateEtnryManager


class TemplateHandler:
    def __init__(self, managers):
        self.__template_entry_manager: TemplateEtnryManager = managers["template-entry"]

    def routes(self):
        return [web.post('/template/entry', self.create),
                web.delete('/template/entry', self.delete),
                web.get('/template/entry', self.get)]

    @json_exception
    async def create(self, request: Request):
        body = await request.json()
        template = self.__template_entry_manager.create(ModelFromDict(body))
        return {"id": template.id, "code": template.code}

    @json_exception
    async def delete(self, request: Request):
        return web.json_response({"code": -1, "result": "not implemented"})

    @json_exception
    async def get(self, request: Request):
        return web.json_response({"code": -1, "result": "not implemented"})