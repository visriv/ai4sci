import chromadb
from chromadb.config import Settings

class ChromaVectorStore:
    def __init__(self, persist_directory: str):
        self.client = chromadb.Client(
            Settings(
                persist_directory=persist_directory,
                is_persistent=True
            )
        )
        self.collection = self.client.get_or_create_collection("log_chunks")

    def add_chunks(self, run_id: str, chunks, embeddings):
        ids = [f"{run_id}_{i}" for i in range(len(chunks))]

        self.collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=[{"run_id": run_id} for _ in chunks]
        )

    def query(self, embedding, top_k=5, run_id=None):
        where = {"run_id": run_id} if run_id else None

        res = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where=where
        )

        out = []
        for doc, meta, dist in zip(
            res["documents"][0],
            res["metadatas"][0],
            res["distances"][0]
        ):
            out.append({
                "text": doc,
                "run_id": meta["run_id"],
                "score": float(1 - dist),  # convert distance → similarity
            })

        return out
