import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingest.mock_runs import generate_mock_runs
from src.retriever.retrieval_pipeline import RetrievalPipeline, RetrievalConfig
from src.utils.yaml_loader import load_yaml
from src.utils.logger import get_logger

logger = get_logger("test_retrieval")

def main():
    cfg_dict = load_yaml("configs/retriever.yaml")
    cfg = RetrievalConfig(**cfg_dict)
    retriever = RetrievalPipeline(cfg)

    # generate run
    run = generate_mock_runs(1)[0]
    logger.info(f"Indexing run: {run.run_id}")

    # index logs
    retriever.index_run(run.run_id, run.logs)

    # try searching
    results = retriever.search(run.run_id, "nan loss")

    logger.info("=== Query Results ===")
    for r in results:
        logger.info(f"[score={r['score']:.3f}] {r['text'][:120]}...")

if __name__ == "__main__":
    main()
