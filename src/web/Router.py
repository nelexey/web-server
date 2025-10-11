from dataclasses import dataclass
from aiohttp import web, hdrs
from typing import List, Callable, Awaitable

HandlerType = Callable[[web.Request], Awaitable[web.StreamResponse]]

http_methods = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "PATCH"
]

@dataclass
class Route:
    method: str
    path: str
    handler: HandlerType

    def __post_init__(self):
        valid_methods = {hdrs.METH_GET, hdrs.METH_POST, hdrs.METH_PUT, 
                        hdrs.METH_DELETE, hdrs.METH_PATCH, hdrs.METH_OPTIONS}
        if self.method.upper() not in valid_methods:
            raise ValueError(f"Invalid HTTP method: {self.method}")

class Router:
    @staticmethod
    async def setup_urls(app: web.Application, urls: List[Route]) -> None:
        for route in urls:
            router_method = getattr(app.router, f"add_{route.method.lower()}")
            router_method(route.path, route.handler)