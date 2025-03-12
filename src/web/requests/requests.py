from typing import Optional, Dict
from .Service import Service

# Инициализация сервиса
some_service = Service("https://example.com/")

async def example_req(param1: Optional[int] = None, 
                      param2: Optional[int] = None) -> Dict:
    """
    Пример запроса к сервису.

    Args:
        param1 (Optional[int]): Первый параметр.
        param2 (Optional[int]): Второй параметр.

    Returns:
        Dict: Данные ответа.
    """
    request_data = {
        'param1': param1,
        'param2': param2,
    }

    # Запрос через метод сервиса
    return await some_service.make_request('GET', data=request_data, uri='new_query')
