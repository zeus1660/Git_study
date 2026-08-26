import asyncio
import httpx


async def get_repository(client, repo_name):
    url = f"https://api.github.com/repos/{repo_name}"

    response = await client.get(url, timeout=10)
    response.raise_for_status()

    return response.json()


async def main():
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            get_repository(client, "python/cpython"),
            get_repository(client, "microsoft/vscode"),
        )

    for data in results:
        print(data["full_name"])


asyncio.run(main())