import random
from aiohttp import web
from typing import Callable, Awaitable

def roulette(cartridge: int = 6, loaded: int = 1) -> Callable:
    if cartridge < 1:
        raise ValueError("cartridge must be >= 1")
    if not (0 <= loaded <= cartridge):
        raise ValueError("loaded must be between 0 and cartridge")

    def middleware(handler: Callable[[web.Request], Awaitable[web.Response]]) -> Callable[[web.Request], Awaitable[web.Response]]:
        async def wrapped(request: web.Request) -> web.Response:
            if loaded == 0:
                return await handler(request)
            if loaded == cartridge:
                return web.Response(status=418, text="Запрос убит в русской рулетке")
            
            pos = random.randrange(cartridge)

            if pos < loaded:
                return web.Response(status=418, text="Запрос убит в русской рулетке")
            return await handler(request)
        return wrapped
    return middleware