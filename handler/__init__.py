from aiohttp import web

from context.exception import BusinessException


class ModelFromDict:
    code = ""
    comment = ""

    def __init__(self, dict):
        self.__dict__.update(dict)


def json_exception(handler):
    async def actual_handle(self, *args):
        try:
            result = await handler(self, *args)
            return web.json_response({"code": 0, "result": result})
        except BusinessException as e:
            import traceback
            traceback.print_exc()
            return web.json_response({"code": e.code, "result": {"message": e.message, "extra": e.extra}})
    return actual_handle
