from typing import Dict, List

from web.handlers.handlers import handle_request

# Define URL route configurations for the web server
urls: List[Dict[str, str]] = [
    {
        'method': 'POST',               # HTTP method type
        'path': '/route_to_handle',     # URL path to handle
        'handler': handle_request    # Function that handles requests to this path
    }
]
