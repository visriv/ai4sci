from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from .registry import load_model
from .monitor import monitor_request, METRICS
from ..agent.agent import RCAAgent
from ..agent.tools.search_logs import make_search_logs_tool
from ..agent.tools.inspect_metrics import inspect_metrics
from src.utils.yaml_loader import load_yaml

from ..retriever.retrieval_pipeline import RetrievalPipeline, RetrievalConfig
from prometheus_client import Gauge, Counter, Histogram, generate_latest
from .worker_pool import WorkerPool
from .autoscaler import Autoscaler

import uuid
from .metrics_prom import REQUESTS, ERRORS, LATENCY, WORKERS, BACKLOG
RESULTS = {}  # job_id → {"status": "queued/running/done", "result": None}


app = FastAPI()


# ------------------------------------------------------
# 1) RCA Handler (runs INSIDE workers, not in endpoint)
# ------------------------------------------------------

def rca_job_handler(job):
    """
    job is a dict with:
        run_summary, metrics, logs, model_tag
    """
    llm_model = load_model(job["model_tag"])

    agent = RCAAgent(
        llm_model=llm_model,
        system_prompt_path="src/agent/prompts/system_prompt.txt",
        tools={},   # bind below
        max_steps=4
    )

    cfg = RetrievalConfig(**load_yaml("configs/retriever.yaml"))
    pipeline = RetrievalPipeline(cfg)

    agent.tools = {
        "search_logs": make_search_logs_tool(pipeline),
        "inspect_metrics": lambda: inspect_metrics(job["metrics"])
    }

    pipeline.index_run("request", job["logs"])

    RESULTS[job["job_id"]]["status"] = "running"

    answer = agent.run(job["run_summary"])

    RESULTS[job["job_id"]]["status"] = "done"
    RESULTS[job["job_id"]]["result"] = answer


# ------------------------------------------------------
# 2) Create WorkerPool + Autoscaler
# ------------------------------------------------------

pool = WorkerPool(
    handler_fn=rca_job_handler,
    min_workers=1,
    max_workers=10,
    monitor=METRICS
)

autoscaler = Autoscaler(pool, METRICS)


# ------------------------------------------------------
# 3) FastAPI Request Model
# ------------------------------------------------------

class RCARequest(BaseModel):
    run_summary: str
    metrics: dict
    logs: list
    model_tag: str = "rca-v2"


# ------------------------------------------------------
# 4) FastAPI /rca endpoint
# ------------------------------------------------------

@app.post("/rca")
def rca_endpoint(req: RCARequest):
    job_id = str(uuid.uuid4())
    RESULTS[job_id] = {"status": "queued", "result": None}

    job = {
        "job_id": job_id,
        "run_summary": req.run_summary,
        "metrics": req.metrics,
        "logs": req.logs,
        "model_tag": req.model_tag
    }

    pool.submit(job)
    return {"status": "queued", "job_id": job_id}


@app.get("/rca/{job_id}")
def get_status(job_id: str):
    if job_id not in RESULTS:
        raise HTTPException(404, "job not found")
    return RESULTS[job_id]


# ------------------------------------------------------
# 5) Metrics endpoint (unchanged)
# ------------------------------------------------------

@app.get("/metrics")
def get_metrics():
    return METRICS


# ------------------------------------------------------
# 6) WorkerPool status endpoint
# ------------------------------------------------------

@app.get("/worker_pool")
def worker_status():
    return {
        "workers": pool.worker_count,
        "backlog": pool.backlog,
        "min_workers": pool.min_workers,
        "max_workers": pool.max_workers,
    }


@app.get("/prometheus")
def prometheus_metrics():
    return Response(generate_latest(), media_type="text/plain")