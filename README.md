<p align="center">
  <img src="images/logo.png" alt="Logo" width="30%"/>
</p>

#

Компонент веб-сервера на Python для лёгкой интеграции в рабочие проекты, создания простой микросервсиной архитектуры и облегчённого взаимодействия между отедльно запущенными компонентами проекта.
Отличается лёгкой интеграцией, фоновой работой, асинхронностью, удобным менеджементом сервисов для взаимодействия.


### Примеры
Пример зарпоса к сайту <a href="https://example.com/">example.com</a>. Код <code>main.py</code> в той же директории, что и <code>web/</code>:
```Python
import asyncio
from web.server import init_web_server
from web.requests.Service import Service

async def main():

    await init_web_server(config={'host': 'localhost', 'port': 8080})
    example = Service('https://example.com')

    resp = await example.make_request(method='GET', data={}, r_type='text')
    
    print(resp)

asyncio.run(main())
```

Результат:
```
<ClientResponse(https://example.com/) [200 OK]>
<CIMultiDictProxy('Accept-Ranges': 'bytes', 'Content-Type': 'text/html', 'Etag': '"84238dfc8092e5d9c0dac8ef93371a07:1736799080.121134"', 'Last-Modified': 'Mon, 13 Jan 2025 20:11:20 GMT', 'Vary': 'Accept-Encoding', 'Content-Encoding': 'gzip', 'Content-Length': '648', 'Cache-Control': 'max-age=3492', 'Date': 'Wed, 12 Mar 2025 11:09:02 GMT', 'Alt-Svc': 'h3=":443"; ma=93600,h3-29=":443"; ma=93600,quic=":443"; ma=93600; v="43"', 'Connection': 'close')>
```
#
Пример 1000 асинхронных запросов к сайту <a href="https://example.com/">example.com</a>. Код <code>main.py</code> в той же директории, что и <code>web/</code>:
```Python
import asyncio
import time
from web.server import init_web_server
from web.requests.Service import Service


# Функции запросов к сервисам этичнее писать в отельных файлах в web/requests/
# Для наглядного примера, функция написана в главном файле
# Рекомендуется всегда оборачивать использование метода make_request в функции, подготавливающие данные для запроса
async def make_request(service, index):
    try:
        async with asyncio.timeout(3):
            await service.make_request('GET', data={}, r_type='text')
            return True
    except asyncio.TimeoutError:
        return False
    except Exception as e:
        return False

async def main():
    await init_web_server(config={'host': 'localhost', 'port': 8080})
    example_service = Service('https://example.com')

    start_time = time.time()
    print("Начало обработки...")

    tasks = [make_request(example_service, i) for i in range(1000)]
    results = await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed_time = end_time - start_time
    success_count = sum(results)

    print(f"Обработка завершена.")
    print(f"Время начала: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"Время окончания: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print(f"Успешных запросов: {success_count}")
    print(f"Время выполнения: {elapsed_time:.2f} секунд")

asyncio.run(main())
```
Результат:
```
Начало обработки...
Обработка завершена.
Время начала: 2025-03-12 14:28:55
Время окончания: 2025-03-12 14:28:59
Успешных запросов: 228
Время выполнения: 3.56 секунд
```
Пояснение:
Количество удачных ответов на запросы или в приницпе количество ответов может отличаться из-за ограничений систем, ограничивающих ответов со стороны сервера (429), таймаутов и возможных сетевых ошибок.
