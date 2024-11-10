from typing import Callable, Awaitable
from aiohttp import web

from web.urls import urls

class WebServer:
    def __init__(self, config: dict) -> None:
        """
        Initialize the web server with configuration settings.

        Args:
            config (dict): Configuration for the web server including host, port, and other settings.
        """
        self.config = config
        self.app = web.Application()
        self.setup_routes()

    def setup_routes(self) -> None:
        """
        Sets up routes defined in the `urls` list, binding each path to its handler.
        """
        for route in urls:
            self.app.router.add_route(
                route['method'],
                route['path'],
                route['handler']
            )

    async def run(self) -> None:
        """
        Starts the web server with configurations provided during initialization.
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
    Initializes and starts the web server with the given configuration.

    Args:
        config (dict): Configuration settings for the server, including host and port.
    """
    server = WebServer(config)
    await server.run()
