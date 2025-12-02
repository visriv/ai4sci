import re
from collections import Counter
from typing import List, Dict, Tuple
from ..utils.logger import get_logger

logger = get_logger("EvalMetrics")

LABELS = ["lr_too_high", "oom", "data_path_missing", "none"]

def normalize_label(label: str) -> str:
    if label not in LABELS:
        return "none"
    return label

def parse_predicted_label(text: str) -> str:
    """
    Heuristic: map free-text RCA report to one of our canonical labels.
    """
    t = text.lower()

    if "learning rate" in t or "lr too high" in t or "nan" in t:
        return "lr_too_high"

    if "out of memory" in t or "oom" in t or "cuda out of memory" in t:
        return "oom"

    if "file not found" in t or "data path" in t or "missing data" in t:
        return "data_path_missing"

    return "none"

def compute_accuracy(pairs: List[Tuple[str, str]]) -> Dict[str, float]:
    """
    pairs: list of (gold_label, pred_label)
    """
    total = len(pairs)
    correct = sum(1 for g, p in pairs if g == p)

    per_class = {lab: {"tp": 0, "n": 0} for lab in LABELS}
    for g, p in pairs:
        g = normalize_label(g)
        p = normalize_label(p)
        per_class[g]["n"] += 1
        if g == p:
            per_class[g]["tp"] += 1

    class_acc = {
        lab: (v["tp"] / v["n"] if v["n"] > 0 else 0.0)
        for lab, v in per_class.items()
    }

    return {
        "overall_acc": correct / total if total > 0 else 0.0,
        "per_class_acc": class_acc,
        "n": total,
    }

def confusion_matrix(pairs: List[Tuple[str, str]]) -> Dict[str, Counter]:
    mat: Dict[str, Counter] = {lab: Counter() for lab in LABELS}
    for g, p in pairs:
        g = normalize_label(g)
        p = normalize_label(p)
        mat[g][p] += 1
    return mat
