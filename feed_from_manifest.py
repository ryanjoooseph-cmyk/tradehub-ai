#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Loads task definitions from manifest.json with robust path and parsing:
- Searches sensible locations (src first), or MANIFEST_PATH env.
- Accepts:
  - a single JSON object with {"features":[...]}
  - a list of task objects
  - multiple JSON objects concatenated (we'll decode them all)
Returns a list[dict] of normalized task dicts: {"feature": str, "title": str, ...}
"""

from __future__ import annotations
import json
from json.decoder import JSONDecodeError, JSONDecoder
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _first_existing(paths: List[Path]) -> Path | None:
    for p in paths:
        if p and p.exists():
            return p
    return None


def _candidate_paths() -> List[Path]:
    here = Path(__file__).resolve().parent            # /opt/render/project/src
    root = here.parent                                 # /opt/render/project
    env_p = os.getenv("MANIFEST_PATH")
    return [
        Path(env_p) if env_p else None,
        here / "manifest.json",
        here / "project" / "manifest.json",
        root / "src" / "manifest.json",
        root / "manifest.json",
        Path.cwd() / "manifest.json",
    ]


def _read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def _raw_decode_all(s: str) -> List[Any]:
    """Decode multiple concatenated JSON objects if present."""
    out: List[Any] = []
    dec = JSONDecoder()
    i = 0
    n = len(s)
    while i < n:
        # skip whitespace
        while i < n and s[i].isspace():
            i += 1
        if i >= n:
            break
        obj, j = dec.raw_decode(s, idx=i)
        out.append(obj)
        i = j
    return out


def _parse_manifest(text: str) -> List[Dict[str, Any]]:
    """Return a list of task dicts from various manifest shapes."""
    try:
        data = json.loads(text)
    except JSONDecodeError:
        # Could be multiple concatenated JSON objects -> decode them all
        objs = _raw_decode_all(text)
        if not objs:
            raise
        # If multiple objects, each may be a feature or a task list/object
        tasks: List[Dict[str, Any]] = []
        for obj in objs:
            tasks.extend(_normalize_any(obj))
        return tasks
    else:
        return _normalize_any(data)


def _normalize_any(data: Any) -> List[Dict[str, Any]]:
    """
    Accepts:
      - {"features":[{"name":..., "tasks":[...]}]}
      - [{"title":...}, ...]  (task list)
      - {"title":...}         (single task)
    Produces a flat list of normalized task dicts.
    """
    tasks: List[Dict[str, Any]] = []

    if isinstance(data, dict):
        if "features" in data and isinstance(data["features"], list):
            for feat in data["features"]:
                fname = (feat.get("name") or feat.get("feature") or "unknown") if isinstance(feat, dict) else "unknown"
                inner = feat.get("tasks", []) if isinstance(feat, dict) else []
                if isinstance(inner, list):
                    for t in inner:
                        if isinstance(t, dict):
                            tasks.append(_normalize_task(t, feature=fname))
                elif isinstance(inner, dict):
                    tasks.append(_normalize_task(inner, feature=fname))
        elif "title" in data or "task" in data:
            tasks.append(_normalize_task(data))
        else:
            # Allow {"tasks":[...]} shape too
            maybe = data.get("tasks")
            if isinstance(maybe, list):
                for t in maybe:
                    if isinstance(t, dict):
                        tasks.append(_normalize_task(t))
    elif isinstance(data, list):
        for t in data:
            if isinstance(t, dict):
                tasks.append(_normalize_task(t))

    return tasks


def _normalize_task(t: Dict[str, Any], *, feature: str | None = None) -> Dict[str, Any]:
    return {
        "feature": feature or t.get("feature") or "general",
        "title": t.get("title") or t.get("task") or "untitled",
        "description": t.get("description") or t.get("desc") or "",
        "priority": t.get("priority", "normal"),
        "meta": t.get("meta", {}),
    }


def load_tasks() -> Tuple