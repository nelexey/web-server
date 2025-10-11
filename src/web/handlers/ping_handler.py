from aiohttp import web
from asyncio import sleep

from ..middlewares import middleware, semaphore, roulette

@middleware(semaphore(10, 10), roulette(6, 1))
async def ping_handler(request: web.Request) -> web.Response:
    await sleep(3)
    return web.Response(text='OK')
