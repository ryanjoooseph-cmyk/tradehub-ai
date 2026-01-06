from __future__ import annotations
from pathlib import Path
import json
from typing import List, Dict, Any

DEFAULT_LOCATIONS = [
    Path("manifest/tasks.json"),
    Path("tasks.json"),
]

def _find_manifest() -> Path | None:
    for p in DEFAULT_LOCATIONS:
        if p.exists():
            return p
    return None

def load_tasks() -> List[Dict[str, Any]]:
    manifest = _find_manifest()
    if not manifest:
        print("[feed] no manifest at manifest/tasks.json or ./tasks.json; returning empty list")
        return []
    try:
        with manifest.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "tasks" in data:
            tasks = data["tasks"]
        elif isinstance(data, list):
            tasks = data
        else:
            print("[feed] manifest format not recognized; expected list or {'tasks': [...]}; returning empty")
            return []
        return [t for t in tasks if isinstance(t, dict)]
    except Exception as e:
        print(f"[feed] error reading manifest {manifest}: {e}; returning empty")
        return []
