import json
import aiohttp
import requests
from ..utils.logger import get_logger
from ..cache.cache import cache_get, cache_set

logger = get_logger("LLMClient")

class LLMClient:
    def __init__(self, model_name, host="http://host.docker.internal:11434"):
        self.model = model_name
        self.url_chat = f"{host}/api/chat"
        logger.info(f"[LLMClient] Initialized with model={model_name}")

    # -----------------------------------------
    # Sync chat (used by fallback simple calls)
    # -----------------------------------------
    def chat(self, messages, max_tokens=256):
        payload = {
            "model": self.model,
            "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
            "stream": False,
            "options": {"num_predict": max_tokens}
        }

        cache_key = {"model": self.model, "messages": payload["messages"], "max_tokens": max_tokens}
        cached = cache_get(cache_key)
        if (cached is not None):
            logger.info("[LLM-Cache] hit (sync)")
            return cached

        logger.info("[LLM] [Sync] Sending request to Ollama...")
        res = requests.post(self.url_chat, json=payload)
        data = res.json()
        text = data.get("message", {}).get("content", "")

        cache_set(cache_key, text)
        return text

    # -----------------------------------------
    # Async chat for batching & parallel tools
    # -----------------------------------------
    async def async_chat(self, messages, max_tokens=256):
        payload = {
            "model": self.model,
            "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
            "stream": False,
            "options": {"num_predict": max_tokens}
        }

        cache_key = {"model": self.model, "messages": payload["messages"], "max_tokens": max_tokens}
        cached = cache_get(cache_key)
        if cached is not None:
            logger.info("[LLM-Cache] hit (async)")
            return cached

        logger.info("[LLM] [Async] Request → Ollama...")

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url_chat, json=payload) as resp:
                data = await resp.json()

        text = data.get("message", {}).get("content", "")
        cache_set(cache_key, text)
        return text

    # -----------------------------------------
    # Batched generation (for BatchManager)
    # -----------------------------------------
    async def generate_batch(self, prompts, model=None, tokens=256):
        model = model or self.model

        async with aiohttp.ClientSession() as session:
            prompt_text = "\n\n".join(
                [f"[INST] {p} [/INST]" for p in prompts]
            )

            payload = {
                "model": model,
                "prompt": prompt_text,
                "stream": False,
                "options": {"num_predict": tokens}
            }

            logger.info(f"[LLM] [Batch] {len(prompts)} prompts → Ollama")

            async with session.post(self.url_chat, json=payload) as resp:
                data = await resp.json()

        # Split by \n\n into individual responses
        outputs = data.get("message", {}).get("content", "").split("\n\n")
        if len(outputs) < len(prompts):
            outputs = outputs + [""] * (len(prompts) - len(outputs))

        return outputs
