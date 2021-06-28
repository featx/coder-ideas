from aiohttp import web
from aiohttp.web_request import Request

from handler import json_exception
from manage.language import LanguageManager


class LanguageHandler:
    def __init__(self, managers):
        self.__language_manager: LanguageManager = managers["language"]

    def routes(self):
        return [web.get('/languages', self.list_all)]

    @json_exception
    async def list_all(self, request: Request):
        return self.__language_manager.list_all()
