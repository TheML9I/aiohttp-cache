import asyncio
import uvloop
import json

from aiohttp import web

from aiohttp_cached import settings
from aiohttp_cached.cache.decorators import cache


def run():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app = web.Application()

    app.router.add_get('/demo', DemoView)
    web.run_app(app, host=settings.PROJECT_HOST, port=settings.PROJECT_PORT)


class DemoView(web.View):
    async def get(self):
        return web.Response(text=json.dumps(await coro_for_cache(ids=[1, 2, 3])))


@cache(key=lambda *args, **kwargs: ','.join(map(str, kwargs['ids'])))
async def coro_for_cache(ids=None):
    # some loaded operation, for instance get rows from db
    return await mess_for_cache(ids)


@asyncio.coroutine
async def mess_for_cache(ids):
    return ['Value One', 'Value Two', 'Value Three']

if __name__ == '__main__':
    run()
