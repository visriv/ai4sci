from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class RunRecord:
    run_id: str
    config: Dict
    logs: List[str]
    metrics: Dict[str, List[float]]
    status: str                # 'success' | 'failed'
    root_cause: Optional[str] = None
    evidence: Optional[List[str]] = None
