from typing import Callable, Awaitable, Any, Tuple
from aiohttp import web

def middleware(*middlewares_list: Callable) -> Callable:
    def decorator(handler: Callable[[web.Request], Awaitable[web.Response]]) -> Callable[[web.Request], Awaitable[web.Response]]:
        current_handler = handler
        for mw in reversed(middlewares_list):
            current_handler = mw(current_handler)
    
        return current_handler
    return decorator