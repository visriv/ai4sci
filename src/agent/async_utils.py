import asyncio

async def gather_dict(tasks: dict):
    """
    Parallel execution for dict of coroutines.
    Returns dict with same keys -> results.
    """
    keys = list(tasks.keys())
    coros = [tasks[k] for k in keys]
    results = await asyncio.gather(*coros, return_exceptions=True)
    return {k: r for k, r in zip(keys, results)}
