from dataclasses import dataclass
from typing import List

from dashboard.components import logs
from ..utils.logger import get_logger
from .chunker import chunk_lines
from .embedder import Embedder
from .vector_store import ChromaVectorStore

logger = get_logger(__name__)

@dataclass
class RetrievalConfig:
    embedding_model: str
    chunk_size: int
    chunk_overlap: int
    top_k: int
    persist_directory: str

class RetrievalPipeline:
    def __init__(self, cfg: RetrievalConfig):
        self.cfg = cfg
        self.embedder = Embedder(cfg.embedding_model)
        self.store = ChromaVectorStore(cfg.persist_directory)

    def index_run(self, run_id: str, logs: List[str]):
        logger.info(f"Indexing run {run_id} with {len(logs)} log lines")

        if not logs:
            return  

        chunks = chunk_lines(
            logs,
            max_lines=self.cfg.chunk_size,
            overlap=self.cfg.chunk_overlap
        )
        embeddings = self.embedder.encode(chunks)

        self.store.add_chunks(run_id, chunks, embeddings)

    def search(self, run_id: str, query: str):
        q_emb = self.embedder.encode([query])[0]
        return self.store.query(q_emb, self.cfg.top_k, run_id)
