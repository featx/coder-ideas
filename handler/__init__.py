from aiohttp import web

import traceback
from context.exception import BusinessException


class ModelFromDict:
    code = ""
    comment = ""

    def __init__(self, diction: dict):
        self.__dict__.update(diction)


def json_exception(handler):
    async def actual_handle(self, *args):
        try:
            result = await handler(self, *args)
            return web.json_response({"code": 0, "result": result})
        except BusinessException as e:
            return web.json_response({"code": e.code, "result": {"message": e.message, "extra": e.extra}})
        except Exception as e:
            traceback.print_exc()
            return web.json_response({"code": 50000, "result": {"message": "Internal error", "extra": ""}})
    return actual_handle
