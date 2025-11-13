# feed_from_manifest.py
# Robust loader for job definitions ("features") from manifest.json or env.
# Accepts:
#   - A JSON object with {"features":[...]}, OR
#   - A JSON list of feature dicts, OR
#   - JSON Lines (one JSON object per line)
#
# Fallbacks:
#   - MANIFEST_JSON (env with raw JSON/JSONL)
#   - A built-in single "example" task

from __future__ import annotations
import json, os, io
from typing import List, Dict, Any

_DEF_TASKS: List[Dict[str, Any]] = [{
    "feature": "example",
    "instructions": "No manifest found; run the example flow only."
}]

def _read_text_from_any(path_candidates: list[str]) -> str | None:
    for p in path_candidates:
        try:
            if p and os.path.exists(p):
                with io.open(p, "r", encoding="utf-8") as f:
                    return f.read()
        except Exception:
            pass
    raw = os.environ.get("MANIFEST_JSON")
    if raw and raw.strip():
        return raw
    return None

def _parse_any_json_shape(src: str) -> List[Dict[str, Any]]:
    # 1) Try single JSON (object or list)
    try:
        parsed = json.loads(src)
        if isinstance(parsed, dict):
            # {"features":[...]} or single feature object
            if "features" in parsed and isinstance(parsed["features"], list):
                items = parsed["features"]
            else:
                items = [parsed]
        elif isinstance(parsed, list):
            items = parsed
        else:
            items = []
        return _normalize_items(items)
    except json.JSONDecodeError:
        pass

    # 2) Try JSON Lines (one object per line)
    items: List[Dict[str, Any]] = []
    for line in src.splitlines():
        line = line.strip()
        if not line or not (line.startswith("{") and line.endswith("}")):
            continue
        try:
            obj = json.loads(line)
            items.append(obj)
        except Exception:
            continue
    if items:
        return _normalize_items(items)

    # 3) Give up -> default
    return _DEF_TASKS[:]

def _normalize_items(items: List[Any]) -> List[Dict[str, Any]]:
    norm: List[Dict[str, Any]] = []
    for it in items:
        if isinstance(it, dict):
            # Accept "feature" or "name" as the label key
            if "feature" not in it and "name" in it:
                it = {"feature": it["name"], **{k: v for k, v in it.items() if k != "name"}}
            # Minimum contract
            if "feature" in it and isinstance(it["feature"], str):
                norm.append(it)
            else:
                # Skip non-conforming dicts
                continue
        else:
            # Skip tuples/strings/etc.
            continue
    return norm if norm else _DEF_TASKS[:]

def load_tasks() -> List[Dict[str, Any]]:
    # Try a bunch of likely locations (Render runs from /opt/render/project)
    cwd = os.getcwd()
    here = os.path.dirname(os.path.abspath(__file__))

    candidates = [
        os.environ.get("MANIFEST_PATH", "").strip() or None,
        os.path.join(cwd, "manifest.json"),
        os.path.join(cwd, "project", "manifest.json"),
        os.path.join(cwd, "src", "manifest.json"),
        os.path.join(os.path.dirname(cwd), "manifest.json"),
        os.path.join(here, "..", "manifest.json"),
        os.path.join(here, "manifest.json"),
        "manifest.json",
    ]
    text = _read_text_from_any([c for c in candidates if c])
    if text is None:
        return _DEF_TASKS[:]
    return _parse_any_json_shape(text)

if __name__ == "__main__":
    tasks = load_tasks()
    print(f"[feed] loaded {len(tasks)} task definitions")
    for t in tasks[:3]:
        print(" -", t.get("feature"))