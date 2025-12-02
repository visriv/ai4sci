from ...retriever.retrieval_pipeline import RetrievalPipeline
from ...utils.logger import get_logger

logger = get_logger("Tool.search_logs")

def make_search_logs_tool(pipeline: RetrievalPipeline):

    def _tool(run_id: str, query: str, top_k: int | None = None):
        logger.info(f"[Tool] [search_logs] run_id={run_id} query='{query}'")

        res = pipeline.search(run_id, query)

        logger.info(f"[Tool] [search_logs] Retrieved {len(res)} chunks")
        return res

    return _tool
