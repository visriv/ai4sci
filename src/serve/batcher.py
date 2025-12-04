import asyncio
import time
from typing import Dict, Any, List
from dataclasses import dataclass, field
from ..utils.logger import get_logger

logger = get_logger("Batcher")

@dataclass
class BatchItem:
    prompt: str
    future: asyncio.Future
    model: str
    tokens: int


class BatchManager:
    def __init__(self, max_batch_size=4, max_wait_ms=40):
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms / 1000
        self.queue: List[BatchItem] = []
        self.lock = asyncio.Lock()
        self.running = False

    async def enqueue(self, prompt: str, model: str, tokens: int) -> str:
        future = asyncio.get_event_loop().create_future()

        async with self.lock:
            self.queue.append(BatchItem(prompt, future, model, tokens))

        return await future  # Wait until result is ready

    async def run(self, llm_client):
        self.running = True
        logger.info("[Batcher] Started background batching loop")

        while self.running:
            await asyncio.sleep(self.max_wait_ms)

            async with self.lock:
                if not self.queue:
                    continue

                batch = self.queue[: self.max_batch_size]
                self.queue = self.queue[self.max_batch_size:]

            prompts = [item.prompt for item in batch]
            models = batch[0].model
            tokens = batch[0].tokens

            logger.info(f"[Batcher] Running batch of size {len(batch)}")

            try:
                # batched request
                responses = llm_client.generate_batch(prompts, model=models, tokens=tokens)

                for item, resp in zip(batch, responses):
                    item.future.set_result(resp)

            except Exception as e:
                for item in batch:
                    item.future.set_exception(e)
