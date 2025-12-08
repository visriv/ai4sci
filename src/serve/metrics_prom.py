from prometheus_client import Counter, Histogram, Gauge

REQUESTS = Counter("scirca_requests_total", "Total RCA requests")
ERRORS = Counter("scirca_errors_total", "Total errors")

LATENCY = Histogram(
    "scirca_latency_ms",
    "Latency of RCA processing (ms)",
    buckets=[50, 100, 200, 500, 1000, 2000]
)

WORKERS = Gauge("scirca_workers", "Active workers")
BACKLOG = Gauge("scirca_backlog", "Queue backlog")
