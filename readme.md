# Async Web Server Template

This Python-based asynchronous web server template is designed for easy integration into other Python scripts, allowing for handling of HTTP requests and making external API calls. 


## Getting Started

### Basic Example

To quickly launch the server and make an example request, use the following setup:

```python
import asyncio
from web.server import init_web_server
from web.requests.Service import Service

async def main():
    # Launch the web server on localhost at port 8080
    await init_web_server(config={'host': 'localhost', 'port': 8080})
    
    # Initialize a service instance for making requests
    example = Service('https://example.com')
    
    # Make a request to the example service
    # Arguments:
    # - method: HTTP method type ('GET' or 'POST')
    # - data: Data to send with the request. For 'GET', it will be included as query parameters;
    #   for 'POST', it will be in the request body.
    # - r_type: Expected response type ('json', 'text', or 'read')
    resp = await example.make_request(method='GET', data={}, r_type='text')
    
    print(resp)

asyncio.run(main())
```

### Advanced Usage

In the following example, the server processes a batch of asynchronous requests, counts successful responses, and records the start and end times:

```python
import asyncio
import time
from web.server import init_web_server
from web.requests.Service import Service

async def make_request(service, index):
    """Helper function to make an individual request and check for success."""
    try:
        await service.make_request('GET', data={}, r_type='text')
        print(f"Request {index + 1} completed successfully.")
        return True
    except Exception as e:
        print(f"Request {index + 1} failed: {e}")
        return False

async def main():
    # Launch the web server
    await init_web_server(config={'host': 'localhost', 'port': 8080})
    example_service = Service('https://example.com')

    start_time = time.time()
    print("Starting batch processing...")

    # Create tasks for 1000 async requests
    tasks = [make_request(example_service, i) for i in range(1000)]
    results = await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed_time = end_time - start_time
    success_count = sum(results)

    print(f"Batch processing completed.")
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print(f"Total successful requests: {success_count}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

asyncio.run(main())
```

