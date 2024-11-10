import json
from aiohttp import web
from typing import Dict

async def handle_request(request: web.Request) -> web.Response:
    """
    Handles the incoming HTTP request, parses the JSON data, validates the required parameters,
    and returns an appropriate response.

    Args:
        request (web.Request): The incoming HTTP request containing JSON data.

    Returns:
        web.Response: The HTTP response, either with success or error message.
    """
    try:
        # Parse JSON data from the request
        data: Dict = await request.json()

    except json.JSONDecodeError:
        # Handle invalid JSON data
        return web.Response(text="Invalid JSON data", status=400)

    # Retrieve and validate 'some_parameter' from the parsed data
    some_parameter = data.get('some_parameter')
    if some_parameter is None:
        # Handle missing 'some_parameter'
        return web.Response(text="Missing 'some_parameter' parameter", status=400)

    # Prepare the response text
    response_text = "Operation completed successfully"

    # Return the final success response
    return web.Response(text=response_text)
