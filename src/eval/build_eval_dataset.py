from pathlib import Path
import json
from typing import List
from ..ingest.mock_runs import generate_mock_runs
from ..ingest.run_schema import RunRecord
from ..utils.logger import get_logger

logger = get_logger("EvalDataset")

def run_to_example(run: RunRecord) -> dict:
    """
    Convert a RunRecord into an eval example with a natural-language summary.
    """
    summary = f"""
Run ID: {run.run_id}
Status: {run.status}
Config: {run.config}
We observed training logs and loss metrics.
If the run failed, explain the most likely root cause and how to fix it.
""".strip()

    return {
        "run_id": run.run_id,
        "run_summary": summary,
        "root_cause": run.root_cause or "none",
        "metrics": run.metrics,
        "logs": run.logs,
    }

def build_eval_dataset(n_runs: int, out_path: str):
    runs: List[RunRecord] = generate_mock_runs(n_runs)
    examples = [run_to_example(r) for r in runs if r.root_cause is not None]

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        for ex in examples:
            json.dump(ex, f)
            f.write("\n")

    logger.info(
        f"[Eval] Built dataset with {len(examples)} labelled examples → {out_path}"
    )

if __name__ == "__main__":
    build_eval_dataset(n_runs=30, out_path="data/rca_dataset/eval.jsonl")
