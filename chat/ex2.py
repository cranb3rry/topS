import aiohttp
import asyncio

url ='https://donate.qiwi.com/api/stream/v1/widgets/fed55c39-a00c-4cd9-a281-9e4dd2663c73/events?queuePriority=ANY&consumerExtId=71f8a709-394a-4170-9b19-58ab7c1dc0a9&limit=2'

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            html = await fetch(session, url)
            print(html)
            await asyncio.sleep(2)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())