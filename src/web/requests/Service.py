import aiohttp
import urllib.parse
from typing import Any, Dict, Optional, Union


class Service:
    """Класс для HTTP запросов."""

    class ResponseError(Exception):
        def __init__(self, status: int, message: str) -> None:
            """
            Исключение для ошибок HTTP.

            Args:
                status (int): Код статуса.
                message (str): Сообщение ошибки.
            """
            self.status = status
            self.message = message
            super().__init__(f"{status}: {message}")

    def __init__(self, url: str) -> None:
        """
        Инициализация сервиса.

        Args:
            url (str): url сервиса, с которым происходит взаимодействие.
        """
        self.url = url

    async def make_request(
        self,
        method: str = 'POST',
        data: Optional[Dict[str, Any]] = None,
        uri: str = '',
        r_type: str = ''
    ) -> Union[str, Dict[str, Any], bytes, aiohttp.ClientResponse]:
        """
        Выполнение HTTP запроса.

        Args:
            method (str): HTTP метод.
            data (dict): Данные запроса.
            uri (str): URI-путь.
            r_type (str): Тип ответа.

        Returns:
            Union[str, Dict[str, Any], bytes, aiohttp.ClientResponse]: Ответ.

        Raises:
            ResponseError: Ошибка соединения.
        """
        # Формируем URL с параметрами
        if method == 'GET' and data:
            query_string = urllib.parse.urlencode(data)
            url = f"{self.url}/{uri}?{query_string}"
        else:
            url = f"{self.url}/{uri}"

        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, json=data) as response:
                    content_type = response.headers.get("Content-Type", "")


                    # Адаптивно преобразовать ответ в зависимости от типа ответа
                    if r_type == 'json' and 'application/json' in content_type:
                        return await response.json()
                    elif r_type == 'text' and 'text/plain' in content_type:
                        return await response.text()
                    elif r_type == 'read':
                        return await response.read()
                    else:
                        return response

            except aiohttp.ClientConnectorError as e:
                raise self.ResponseError(status=0, message=str(e))
