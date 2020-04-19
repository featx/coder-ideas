from aiohttp import web


class ModelFromDict:
    comment = ""

    def __init__(self, dict):
        self.__dict__.update(dict)


def json_exception(handler):
    async def actual_handle(*args):
        try:
            result = await handler(*args)
            return web.json_response({"code": 0, "result": result})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return web.json_response({"code": -1, "result": {"message": "", "tips": ""}})
    return actual_handle
