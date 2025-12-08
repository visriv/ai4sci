import time
from functools import wraps
from ..utils.logger import get_logger

logger = get_logger("Monitor")


METRICS = {
    "requests_total": 0,
    "errors_total": 0,
    "latency_ms": [],
    "history": {
        "timestamp": [],
        "workers": [],
        "backlog": [],
        "p95_latency": []
    }
}

def record_history(workers, backlog, p95):
    METRICS["history"]["timestamp"].append(time.time())
    METRICS["history"]["workers"].append(workers)
    METRICS["history"]["backlog"].append(backlog)
    METRICS["history"]["p95_latency"].append(p95)



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
