import random
from typing import List
from .run_schema import RunRecord

FAILURES = [
    ("lr_too_high", "Loss diverged to NaN."),
    ("data_path_missing", "Dataloader could not find dataset."),
    ("oom", "CUDA out of memory."),
]

def generate_mock_run(run_id: int) -> RunRecord:
    random.seed(run_id)

    lr = random.choice([1e-1, 1e-2, 1e-3])
    batch_size = random.choice([16, 32, 64, 128, 512])

    config = {"lr": lr, "batch_size": batch_size, "model": "resnet18"}

    logs = []
    metrics = {"loss": []}
    status = "success"
    root_cause = None
    evidence = []

    loss = 2.0
    for step in range(80):
        if lr == 1e-1 and step > 20:
            logs.append(f"Step {step}: loss=nan")
            metrics["loss"].append(float("nan"))
            status = "failed"
            root_cause = "lr_too_high"
            evidence.append("Loss became NaN after step ~20.")
            break
        
        loss *= 0.98
        logs.append(f"Step {step}: loss={loss:.3f}")
        metrics["loss"].append(loss)

    if status == "success" and batch_size >= 256:
        logs.append("RuntimeError: CUDA out of memory on device 0")
        status = "failed"
        root_cause = "oom"
        evidence.append("Batch size too large causing OOM.")

    if status == "success" and random.random() < 0.1:
        logs.append("FileNotFoundError: /data/train/images missing")
        status = "failed"
        root_cause = "data_path_missing"
        evidence.append("Dataset folder missing or path incorrect.")

    return RunRecord(
        run_id=f"run_{run_id}",
        config=config,
        logs=logs,
        metrics=metrics,
        status=status,
        root_cause=root_cause,
        evidence=evidence or None
    )

def generate_mock_runs(n: int) -> List[RunRecord]:
    return [generate_mock_run(i) for i in range(n)]
