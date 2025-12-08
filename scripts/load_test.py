# scripts/load_test.py
import asyncio
import aiohttp
import argparse
import random
import time

async def send_one(session, api):
    payload = {
        "summary": "OOM in Step " + str(random.randint(1,100)),
        "logs": ["CUDA error", "Killed"],
        "metrics": {"gpu": 98, "batch": 256}
    }
    async with session.post(f"{api}/rca", json=payload) as r:
        return await r.json()

async def main(api, concurrency, total):
    async with aiohttp.ClientSession() as session:
        tasks = []

        for _ in range(total):
            tasks.append(asyncio.create_task(send_one(session, api)))

            if len(tasks) >= concurrency:
                await asyncio.gather(*tasks)
                tasks = []

        if tasks:
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", default="http://localhost:8000")
    parser.add_argument("--concurrency", type=int, default=20)
    parser.add_argument("--total", type=int, default=200)
    args = parser.parse_args()

    asyncio.run(main(args.api, args.concurrency, args.total))
