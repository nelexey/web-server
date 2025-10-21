import asyncio
from web import Server, BaseClient

async def main() -> None:
    main_server = Server('localhost', 8080)
    
    await main_server.start()

    wttr = BaseClient('https://wttr.in/')

    print(await wttr.request('Москва', data={'format': 3}))

    while True:
        await asyncio.sleep(3600)


if __name__=="__main__":
    asyncio.run(main())