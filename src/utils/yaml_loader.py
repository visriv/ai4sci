from pathlib import Path
from typing import Any, Dict
import yaml

def load_yaml(path: str | Path) -> Dict[str, Any]:
    """
    Load a YAML configuration file and return a Python dict.

    Example:
        cfg = load_yaml("configs/retriever.yaml")
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r") as f:
        return yaml.safe_load(f)
