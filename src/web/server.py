from aiohttp import web
from typing import List
from .Router import Router, Route
from .urls import urls

class Server:
    def __init__(self, 
                 host: str = 'localhost', 
                 port: int = 8080, 
                 urls: List[Route] = urls) -> None:
        
        self.host = host
        self.port = port
        self.urls = urls
        self.app = web.Application()

    async def start(self) -> None:
        await Router.setup_urls(self.app, self.urls)

        runner = web.AppRunner(self.app)
        
        await runner.setup()

        await web.TCPSite(runner, 
                    host=self.host, 
                    port=self.port).start()

    async def stop(self) -> None:
        await self.app.shutdown()
        await self.app.cleanup()
