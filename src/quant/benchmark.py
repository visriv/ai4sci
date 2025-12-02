import time
import requests
from ..utils.logger import get_logger

logger = get_logger("QuantBench")

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def run_generation(model: str, prompt: str, tokens: int = 256) -> dict:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": tokens}
    }

    start = time.time()
    resp = requests.post(OLLAMA_URL, json=payload).json()
    end = time.time()

    text = resp.get("response", "")
    elapsed = end - start
    tok_per_sec = tokens / elapsed if elapsed > 0 else 0

    return {
        "model": model,
        "time": elapsed,
        "tps": tok_per_sec,
        "chars": len(text),
        "preview": text[:200]
    }

def benchmark_models(models: list[str], prompt: str, tokens: int = 256):
    logger.info(f"[Bench] Starting benchmark on {len(models)} models")
    results = []

    for m in models:
        logger.info(f"[Bench] Testing model: {m}")
        res = run_generation(m, prompt, tokens)
        logger.info(f"[Bench] Model={m} | {res['tps']:.1f} tok/s | time={res['time']:.2f}s")
        results.append(res)

    logger.info("[Bench] Benchmark complete")
    return results
