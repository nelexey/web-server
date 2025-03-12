import json
from aiohttp import web
from typing import Dict

async def handle_request(request: web.Request) -> web.Response:
    """
    Обработка входящих запросов.

    Args:
        request (web.Request): Запрос.

    Returns:
        web.Response: Ответ.
    """
    try:
        data: Dict = await request.json()

    except json.JSONDecodeError:
        return web.Response(text="Invalid JSON data", status=400)

    # Проверка параметра на наличие
    some_parameter = data.get('some_parameter')
    if some_parameter is None:
        return web.Response(text="Missing 'some_parameter' parameter", status=400)
    
    return web.Response(text="Operation completed successfully")
