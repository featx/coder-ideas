# from aiohttp import web

from context.context import CoderApplication


# class UserHandler:
#     def __init__(self):
#         routes = web.RouteTableDef()
#
#     @routes.get("/{name}")
#     async def handle(request):
#         name = request.match_info.get('name', "Anonymous")
#         text = "Hello, " + name
#         return web.Response(text=text)
#
#
#
# app = web.Application()
# app.add_routes(routes)
# web.run_app(app)
if __name__ == '__main__':
    CoderApplication().start()
