from .Router import Route

from .handlers.ping_handler import ping_handler

urls = [
    Route('GET', '/ping', ping_handler)
]
