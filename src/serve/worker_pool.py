import queue
import threading
import time
from .metrics_prom import LATENCY, WORKERS, BACKLOG


class WorkerPool:
    def __init__(self, handler_fn, min_workers=1, max_workers=10, monitor=None):
        self.handler_fn = handler_fn
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.monitor = monitor

        self.queue = queue.Queue()
        self.workers = []
        self.running = True
        self.lock = threading.Lock()

        # spin up initial workers
        for _ in range(self.min_workers):
            self._add_worker()

    def _add_worker(self):
        t = threading.Thread(target=self._worker_loop, daemon=True)
        t.start()
        self.workers.append(t)

    def _worker_loop(self):
        while self.running:
            jobs = []

            # always take at least one job
            try:
                jobs.append(self.queue.get(timeout=1))
            except queue.Empty:
                continue

            # try to collect more jobs
            for _ in range(3):  # batch size = 4
                try:
                    jobs.append(self.queue.get_nowait())
                except queue.Empty:
                    break

            start = time.time()
            try:
                # process batch
                for job in jobs:
                    self.handler_fn(job)
            finally:
                latency = (time.time() - start) * 1000
                self.monitor["latency_ms"].append(latency)


                LATENCY.observe(latency)
                WORKERS.set(self.worker_count)
                BACKLOG.set(self.backlog)

                for _ in jobs:
                    self.queue.task_done()

    def submit(self, job: dict):
        self.queue.put(job)

    def scale_up(self):
        with self.lock:
            if len(self.workers) < self.max_workers:
                self._add_worker()

    def scale_down(self):
        with self.lock:
            if len(self.workers) > self.min_workers:
                self.workers.pop()

    @property
    def backlog(self):
        return self.queue.qsize()

    @property
    def worker_count(self):
        return len(self.workers)
