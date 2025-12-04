import json
from pathlib import Path

REGISTRY_PATH = Path("registry")

def load_model(tag: str) -> str:
    """
    Returns: ollama model name (e.g., 'llama3:8b-instruct')
    """
    f = REGISTRY_PATH / f"{tag}.json"
    if not f.exists():
        raise RuntimeError(f"Model tag '{tag}' not found in registry")
    return json.loads(f.read_text())["model_name"]

def register_model(tag: str, model_name: str):
    REGISTRY_PATH.mkdir(exist_ok=True)
    data = {"model_name": model_name}
    (REGISTRY_PATH / f"{tag}.json").write_text(json.dumps(data, indent=2))

def promote_model(tag: str):
    """
    Sets the given tag as the 'best' production model.
    """
    (REGISTRY_PATH / "best.json").write_text(
        json.dumps({"model_name": load_model(tag)}, indent=2)
    )
