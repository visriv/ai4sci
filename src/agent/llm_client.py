import requests
import json
from ..utils.logger import get_logger

logger = get_logger("LLMClient")

class LLMClient:
    """
    Local LLM client using Ollama’s /api/chat endpoint.
    Fully compatible with SciRCA agent.
    """
    def __init__(self, model_name: str, host: str = "http://127.0.0.1:11434"):
        self.model_name = model_name
        self.url = f"{host}/api/chat"

        logger.info(f"[LLM] Using local model: {model_name}")
        logger.info(f"[LLM] Endpoint: {self.url}")

    def chat(self, messages, temperature: float = 0.0):
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
            }
        }

        logger.info("[LLM] Sending request to Ollama...")

        try:
            resp = requests.post(self.url, json=payload)
        except Exception as e:
            logger.error(f"[LLM] Connection error: {e}")
            raise

        if resp.status_code != 200:
            logger.error(f"[LLM] API Error: {resp.text}")
            raise RuntimeError(f"Ollama API error: {resp.text}")

        reply = resp.json()["message"]["content"]

        logger.info(f"[LLM] Response received ({len(reply)} chars)")
        return reply
