import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingest.mock_runs import generate_mock_runs
from src.retriever.retrieval_pipeline import RetrievalPipeline, RetrievalConfig
from src.agent.tools.search_logs import make_search_logs_tool
from src.agent.tools.inspect_metrics import inspect_metrics
from src.agent.agent import RCAAgent
from src.utils.yaml_loader import load_yaml
from src.utils.logger import get_logger

logger = get_logger("AgentDemo")

def main():
    retr_cfg = load_yaml("configs/retriever.yaml")
    cfg = RetrievalConfig(**retr_cfg)
    pipeline = RetrievalPipeline(cfg)

    # generate runs
    run = generate_mock_runs(1)[0]

    # index logs
    logger.info("[Step A] Indexing logs for run")
    pipeline.index_run(run.run_id, run.logs)

    tools = {
        "search_logs": make_search_logs_tool(pipeline),
        "inspect_metrics": lambda: inspect_metrics(run.metrics)
    }

    agent = RCAAgent(
        llm_model="llama3",     # ← most stable general Llama 3
        system_prompt_path="src/agent/prompts/system_prompt.txt",
        tools=tools,
        max_steps=4,
    )

    run_summary = f"""
Run ID: {run.run_id}
Status: {run.status}
Config: {run.config}
Observations: Model produced logs and metrics.
If failure occurred, diagnose root cause.
"""

    logger.info("[Step B] Running agent for RCA...")
    report = agent.run(run_summary)

    print("\n======== RCA REPORT ========\n")
    print(report)
    print("\n============================\n")

if __name__ == "__main__":
    main()
