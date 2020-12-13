from aiohttp import web
from aiohttp.web_request import Request

from handler import json_exception
from manage.framework import FrameworkManager


class FrameworkHandler:
    def __init__(self, managers):
        self.__framework_manager: FrameworkManager = managers["framework"]

    def routes(self):
        return [web.get('/frameworks', self.list_all)]

    @json_exception
    async def list_all(self, request: Request):
        return self.__framework_manager.list_all()