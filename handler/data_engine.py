from aiohttp import web
from aiohttp.web_request import Request

from handler import json_exception, ModelFromDict
from manage.data_engine import DataEngineManager


class DataEngineHandler:
    def __init__(self, managers):
        self.__data_engine_manager: DataEngineManager = managers["data-engine"]

    def routes(self):
        return [web.post('/data-engine', self.create),
                web.delete('/data-engine', self.delete),
                web.get('/data-engine', self.get),
                web.get('/data-engines', self.list_all),
                web.post('/project/data-engine', self.create_for_project),
                web.delete('/project/data-engine', self.delete_of_project),
                web.get('/project/data-engine', self.get_of_project)]

    @json_exception
    async def create(self, request: Request):
        body = await request.json()
        template = self.__data_engine_manager.create(ModelFromDict(body))
        return {"id": template.id, "code": template.code}

    @json_exception
    async def delete(self, request: Request):
        return web.json_response({"code": -1, "result": "not implemented"})

    @json_exception
    async def get(self, request: Request):
        return web.json_response({"code": -1, "result": "not implemented"})

    @json_exception
    async def list_all(self, request: Request):
        return self.__data_engine_manager.list_all()

    @json_exception
    async def create_for_project(self, request: Request):
        body = await request.json()
        data_engine = self.__data_engine_manager.create_project_data_engine(ModelFromDict(body))
        return {"id": data_engine.id, "code": data_engine.code}

    @json_exception
    async def delete_of_project(self, request: Request):
        return web.json_response({"code": -1, "result": "not implemented"})

    @json_exception
    async def get_of_project(self, request: Request):
        return web.json_response({"code": -1, "result": "not implemented"})
