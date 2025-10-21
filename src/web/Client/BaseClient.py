import aiohttp
from typing import Dict, Any, Optional, Literal, Union, Callable, Awaitable


ResponseType = Literal["json", "text", "html", "bytes"]

class BaseClient:
    def __init__(
        self, 
        base_url: str, 
        default_headers: Optional[Dict[str, str]] = None,
        timeout: float = 10.0
    ):
        self._base_url = base_url.rstrip('/')
        self._default_headers = default_headers or {}
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers=self._default_headers,
                timeout=self._timeout
            )
        return self._session

    async def __aenter__(self):
        await self._get_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def request(
        self, 
        uri: str, 
        method: str = 'GET', 
        data: Optional[Dict[str, Any]] = None, 
        response_type: Optional[ResponseType] = None,
        **kwargs
    ) -> Union[Dict[str, Any], str, bytes]:
        
        full_url = f"{self._base_url}/{uri.lstrip('/')}"
        session = await self._get_session()
        request_kwargs = kwargs.copy()
        
        if data:
            if method in ["GET", "HEAD"]:
                request_kwargs['params'] = data
            elif 'json' not in request_kwargs and 'data' not in request_kwargs:
                request_kwargs['json'] = data
        
        async with session.request(method, full_url, **request_kwargs) as response:
            
            if response.status >= 400:
                error_body = await response.text()
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=f"HTTP Error: {response.status}",
                    headers=response.headers,
                ) from Exception(error_body)

            parsers: Dict[ResponseType, Callable[[], Awaitable[Union[Dict, str, bytes]]]] = {
                "json": response.json,
                "text": response.text,
                "html": response.text, 
                "bytes": response.read
            }

            if response_type:
                if response_type not in parsers:
                    raise ValueError(f"Unknown response type: {response_type}")
                return await parsers[response_type]()
            
            content_type = response.content_type.lower()
            
            if 'json' in content_type:
                return await response.json()
            elif 'text' in content_type or 'html' in content_type:
                return await response.text()
            else:
                return await response.read()