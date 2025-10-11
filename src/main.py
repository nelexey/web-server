import asyncio
from web import Server
import aiohttp

async def main() -> None:
    main_server = Server('localhost', 8080)
    
    await main_server.start()

    while True:
        await asyncio.sleep(3600)


if __name__=="__main__":
    asyncio.run(main())