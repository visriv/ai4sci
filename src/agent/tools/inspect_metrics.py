from ...utils.logger import get_logger
import math

logger = get_logger("Tool.inspect_metrics")

def inspect_metrics(metrics: dict):
    logger.info("[Tool] [inspect_metrics] Inspecting metrics...")

    out = {}
    loss = metrics.get("loss")

    if loss:
        if any(math.isnan(v) for v in loss):
            out["loss_status"] = "nan_detected"
        elif loss[-1] > loss[0]:
            out["loss_status"] = "diverging"
        else:
            out["loss_status"] = "stable"

    logger.info(f"[Tool] [inspect_metrics] status={out}")
    return out
