import time
from functools import wraps
from ..utils.logger import get_logger

logger = get_logger("Monitor")

# in-memory metrics for now
METRICS = {
    "requests_total": 0,
    "errors_total": 0,
    "latency_ms": [],
}

def monitor_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        METRICS["requests_total"] += 1
        start = time.time()

        try:
            out = func(*args, **kwargs)
        except Exception as e:
            METRICS["errors_total"] += 1
            logger.error(f"[Monitor] error={e}")
            raise

        ms = (time.time() - start) * 1000
        METRICS["latency_ms"].append(ms)

        logger.info(f"[Monitor] latency={ms:.1f}ms requests={METRICS['requests_total']}")
        return out

    return wrapper
