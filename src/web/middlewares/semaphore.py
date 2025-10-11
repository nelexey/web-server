import asyncio
from aiohttp import web
from typing import Callable, Awaitable, Union

def semaphore(max_count: int = 100, timeout: float = 2.0) -> Callable:
    def middleware(handler: Callable[[web.Request], Awaitable[web.Response]]) -> Callable[[web.Request], Awaitable[web.Response]]:
        sem = asyncio.Semaphore(max_count)

        async def wrapped(request: web.Request) -> web.Response:
            try:
                await asyncio.wait_for(sem.acquire(), timeout)
            except asyncio.TimeoutError:
                return web.Response(status=429, text="Too Many Requests")
            try:
                return await handler(request)
            finally:
                sem.release()
        return wrapped
    return middleware