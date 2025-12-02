import json
from pathlib import Path
from typing import List, Dict, Tuple

from ..agent.agent import RCAAgent
from ..agent.tools.search_logs import make_search_logs_tool
from ..agent.tools.inspect_metrics import inspect_metrics
from ..retriever.retrieval_pipeline import RetrievalPipeline, RetrievalConfig
from ..utils.yaml_loader import load_yaml
from ..utils.logger import get_logger
from .metrics import parse_predicted_label, compute_accuracy, confusion_matrix

logger = get_logger("Evaluator")

def load_eval_data(path: str) -> List[Dict]:
    data = []
    with open(path) as f:
        for line in f:
            data.append(json.loads(line))
    logger.info(f"[Eval] Loaded {len(data)} examples from {path}")
    return data

def make_agent() -> RCAAgent:
    retr_cfg = load_yaml("configs/retriever.yaml")
    cfg = RetrievalConfig(**retr_cfg)
    pipeline = RetrievalPipeline(cfg)

    tools = {
        "search_logs": make_search_logs_tool(pipeline),
        # inspect_metrics will be wrapped per-example to inject metrics
    }

    agent = RCAAgent(
        llm_model="llama3",  # or whatever model name you pulled
        system_prompt_path="src/agent/prompts/system_prompt.txt",
        tools=tools,
        max_steps=4,
    )
    return agent, pipeline

def evaluate(dataset_path: str):
    data = load_eval_data(dataset_path)
    agent, pipeline = make_agent()

    pairs: List[Tuple[str, str]] = []

    for ex in data:
        run_id = ex["run_id"]
        logs = ex["logs"]
        metrics = ex["metrics"]
        gold = ex["root_cause"] or "none"

        # index logs per run
        logger.info(f"[Eval] Indexing logs for {run_id}")
        pipeline.index_run(run_id, logs)

        # create per-example inspect_metrics tool
        def inspect_metrics_bound():
            return inspect_metrics(metrics)

        agent.tools["inspect_metrics"] = inspect_metrics_bound

        logger.info(f"[Eval] Running agent for {run_id}")
        pred_report = agent.run(ex["run_summary"])
        pred_label = parse_predicted_label(pred_report)

        logger.info(
            f"[Eval] run_id={run_id} gold={gold} pred={pred_label}"
        )

        pairs.append((gold, pred_label))

    stats = compute_accuracy(pairs)
    mat = confusion_matrix(pairs)

    logger.info("======== Evaluation Summary ========")
    logger.info(f"Overall accuracy: {stats['overall_acc']:.3f} (n={stats['n']})")
    logger.info("Per-class accuracy:")
    for lab, acc in stats["per_class_acc"].items():
        logger.info(f"  {lab:16s}: {acc:.3f}")

    logger.info("Confusion matrix (gold → predicted counts):")
    for g, row in mat.items():
        row_str = ", ".join(f"{p}:{c}" for p, c in row.items())
        logger.info(f"  {g:16s} -> {row_str}")

    return stats, mat

if __name__ == "__main__":
    evaluate("data/rca_dataset/eval.jsonl")
