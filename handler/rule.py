from aiohttp import web
from aiohttp.web_request import Request

from handler import json_exception, ModelFromDict
from manage.rule import TemplateRuleManager


class RuleHandler:
    def __init__(self, managers):
        self.__template_rule_manager: TemplateRuleManager = managers["template-rule"]

    def routes(self):
        return [web.post('/template/rule', self.create),
                web.delete('/template/rule', self.delete),
                web.get('/template/rule', self.get)]

    @json_exception
    async def create(self, request: Request):
        body = await request.json()
        rule = self.__template_rule_manager.create(CreatingTemplateRule(body))
        return {"id": rule.id, "code": rule.code}

    @json_exception
    async def delete(self, request: Request):
        return web.json_response({"code": -1, "result": "not implemented"})

    @json_exception
    async def get(self, request: Request):
        return web.json_response({"code": -1, "result": "not implemented"})


class CreatingTemplateRule(ModelFromDict):
    engine = 0
    type = 0
