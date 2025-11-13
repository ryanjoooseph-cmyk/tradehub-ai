# feed_from_manifest.py
# Harden manifest ingestion. Accepts strings OR dict items in the manifest list.

import json
from typing import Any, Dict, List, Union
from pathlib import Path

MANIFEST_PATH = Path(__file__).resolve().parent.parent / "manifest.json"

def _as_task(item: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(item, str):
        return {"feature": item, "payload": {"feature": item}}
    if isinstance(item, dict):
        feature = item.get("feature") or item.get("name") or "unnamed"
        payload = item.get("payload", {})
        # allow simple dict manifest entries to be the payload
        if not payload and any(k for k in item.keys() if k not in ("feature","name","payload")):
            payload = {k: v for k, v in item.items() if k not in ("feature","name","payload")}
        return {"feature": feature, "payload": payload}
    # unknown type → stringify
    return {"feature": "unknown", "payload": {"raw": str(item)}}

def load_tasks() -> List[Dict[str, Any]]:
    raw = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    # raw may be {"tasks":[...]} or just [...]
    items = raw.get("tasks") if isinstance(raw, dict) and "tasks" in raw else raw
    if not isinstance(items, list):
        raise ValueError("manifest.json must be a list or an object with 'tasks' list")
    return [_as_task(it) for it in items]

if __name__ == "__main__":
    tasks = load_tasks()
    print(f"[feed] loaded {len(tasks)} task definitions")