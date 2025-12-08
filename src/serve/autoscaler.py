import threading
import time
import numpy as np

class Autoscaler:
    def __init__(self, worker_pool, monitor, interval=2):
        self.pool = worker_pool
        self.monitor = monitor
        self.interval = interval

        t = threading.Thread(target=self._loop, daemon=True)
        t.start()

    def _p95(self):
        lat = self.monitor["latency_ms"]
        if len(lat) < 5:
            return 0
        return float(np.percentile(lat[-100:], 95))

    def _loop(self):
        while True:
            backlog = self.pool.backlog
            p95 = self._p95()

            from .monitor import record_history

            record_history(
                workers=self.pool.worker_count,
                backlog=backlog,
                p95=p95
            )

            # scale up on pressure
            if backlog > 3 or p95 > 1200:  # 1.2 seconds
                self.pool.scale_up()

            # scale down when idle
            if backlog == 0 and p95 < 500:
                self.pool.scale_down()

            time.sleep(self.interval)
