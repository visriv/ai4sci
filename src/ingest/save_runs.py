import json
from pathlib import Path
from typing import List
from .run_schema import RunRecord

def save_runs(runs: List[RunRecord], out_path: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w") as f:
        for r in runs:
            item = {
                "run_id": r.run_id,
                "config": r.config,
                "logs": r.logs,
                "metrics": r.metrics,
                "status": r.status,
                "root_cause": r.root_cause,
                "evidence": r.evidence,
            }
            json.dump(item, f)
            f.write("\n")

    print(f"[✓] Saved {len(runs)} runs to {out_path}")
