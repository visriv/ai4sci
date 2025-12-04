from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .registry import load_model
from .monitor import monitor_request
from ..agent.agent import RCAAgent
from ..agent.tools.search_logs import make_search_logs_tool
from ..agent.tools.inspect_metrics import inspect_metrics
from src.utils.yaml_loader import load_yaml

app = FastAPI()

class RCARequest(BaseModel):
    run_summary: str
    metrics: dict
    logs: list
    model_tag: str = "rca-v2"

@app.post("/rca")
@monitor_request
def rca_endpoint(req: RCARequest):
    try:
        llm_model = load_model(req.model_tag)

        agent = RCAAgent(
            llm_model=llm_model,
            system_prompt_path="src/agent/prompts/system_prompt.txt",
            tools={},   # bound below
            max_steps=4
        )

        # bind tools dynamically
        from ..retriever.retrieval_pipeline import RetrievalPipeline, RetrievalConfig
        cfg = RetrievalConfig(**load_yaml("configs/retriever.yaml"))
        pipeline = RetrievalPipeline(cfg)

        agent.tools = {
            "search_logs": make_search_logs_tool(pipeline),
            "inspect_metrics": lambda: inspect_metrics(req.metrics)
        }

        # index logs
        pipeline.index_run("request", req.logs)

        answer = agent.run(req.run_summary)

        return { "root_cause_report": answer }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
