import asyncio
from web.server import init_web_server
from web.requests.Service import Service

async def main():

    await init_web_server(config={'host': 'localhost', 'port': 8080})
    example = Service('https://example.com')

    resp = await example.make_request(method='GET', data={}, r_type='text')
    
    print(resp)

asyncio.run(main())