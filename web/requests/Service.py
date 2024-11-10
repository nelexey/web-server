import aiohttp
import urllib.parse
from typing import Any, Dict, Optional, Union


class Service:
    """A class to configure and execute HTTP requests to an API."""

    class ResponseError(Exception):
        def __init__(self, status: int, message: str) -> None:
            """
            Exception for handling HTTP response errors.

            Args:
                status (int): HTTP status code of the error.
                message (str): Error message describing the issue.
            """
            self.status = status
            self.message = message
            super().__init__(f"{status}: {message}")

    def __init__(self, url: str) -> None:
        """
        Initializes the Service with a base URL.

        Args:
            url (str): Base URL for the API requests.
        """
        self.url = url

    async def make_request(
        self,
        method: str = 'POST',
        data: Optional[Dict[str, Any]] = None,
        uri: str = '',
        r_type: str = 'text'
    ) -> Union[str, Dict[str, Any], bytes, aiohttp.ClientResponse]:
        """
        Executes an HTTP request and returns the result in the specified format.

        Args:
            method (str): HTTP method to use for the request (e.g., 'POST', 'GET').
            data (Optional[Dict[str, Any]]): Data to send with the request.
            uri (str): URI to append to the base URL.
            r_type (str): Expected response type ('json', 'text', 'read') '' by default.

        Returns:
            Union[str, Dict[str, Any], bytes, aiohttp.ClientResponse]: Response content based on `r_type`.

        Raises:
            ResponseError: If there is a connection error or response parsing issue.
        """
        # Construct URL with query parameters for GET requests
        if method == 'GET' and data:
            query_string = urllib.parse.urlencode(data)
            url = f"{self.url}/{uri}?{query_string}"
        else:
            url = f"{self.url}/{uri}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, url, json=data) as response:
                    content_type = response.headers.get("Content-Type", "")

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
