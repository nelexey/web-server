from typing import Callable, Awaitable
from aiohttp import web

from web.urls import urls

class WebServer:
    def __init__(self, config: dict) -> None:
        """
        Инициализация сервера.
        
        Args:
            config (dict): host, port сервера (+ timeout, max_connections)
        """
        self.config = config
        self.app = web.Application()
        self.setup_routes()

    def setup_routes(self) -> None:
        """
        Настройка маршрутов.
        """
        for route in urls:
            self.app.router.add_route(
                route['method'],
                route['path'],
                route['handler']
            )

    async def run(self) -> None:
        """
        Запуск сервера.
        """
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(
            runner,
            self.config['host'],
            self.config['port'],
            shutdown_timeout=self.config.get('timeout', 60),
            backlog=self.config.get('max_connections', 128)
        )
        await site.start()

async def init_web_server(config: dict) -> None:
    """
    Инициализация и запуск сервера.
    
    Args:
        config (dict): Настройки.
    """
    server = WebServer(config)
    await server.run()
