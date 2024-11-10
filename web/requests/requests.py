from typing import Optional, Dict
from .Service import Service

# Initialize the service with a specific URL from the environment settings
some_service = Service("https://example.com/")

async def example_req(param1: Optional[int] = None, param2: Optional[int] = None) -> Dict:
    """
    Example function to make a POST request to 'some_service' with given parameters.

    Args:
        param1 (Optional[int]): First parameter to send in the request data.
        param2 (Optional[int]): Second parameter to send in the request data.

    Returns:
        Dict: JSON response data from the service.
    """
    request_data = {
        'param1': param1,
        'param2': param2,
    }

    # Make a POST request to the specified URI and return the response
    return await some_service.make_request('GET', data=request_data, uri='new_query')
