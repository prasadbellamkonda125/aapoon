import asyncio
import aiohttp


async def download_url(session, queue):
    while True:
        url = await queue.get()
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()
                print(f"Downloaded content from {url}:")
                print(content)
            else:
                print(f"Failed to download {url}: {response.status}")
        queue.task_done()


async def main():
    # Accept list of URLs as input from the user
    urls = []
    num_urls = int(input("Enter the number of URLs: "))
    for i in range(num_urls):
        urls.append(input(f"Enter URL {i + 1}: "))

    max_concurrent_downloads = int(input("Enter the maximum number of concurrent downloads: "))

    queue = asyncio.Queue()
    sem = asyncio.Semaphore(max_concurrent_downloads)

    for url in urls:
        await queue.put(url)

    async with aiohttp.ClientSession() as session:
        tasks = [download_url(session, queue) for _ in range(max_concurrent_downloads)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
