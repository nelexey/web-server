from typing import Dict, List

from web.handlers.handlers import handle_request

urls: List[Dict[str, str]] = [
    {
        'method': 'POST',
        'path': '/route_to_handle',
        'handler': handle_request
    }
]
