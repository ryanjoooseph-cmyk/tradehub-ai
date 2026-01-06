from __future__ import annotations
import json, os
from typing import List, Dict, Any

_DEFAULT_QUEUE = [
    {"task_type":"codegen_backend","feature":"disputes_backend_326","route":"/api/disputes","notes":"Open/list/update disputes; evidence_urls array; status OPEN/REVIEW/RESOLVED"},
    {"task_type":"codegen_frontend","feature":"admin_disputes_frontend_321","route":"/admin/disputes/321","notes":"Admin table with filters; actions to update status; calls /api/disputes"}
]

def load_tasks() -> List[Dict[str, Any]]:
    path = os.path.join(os.path.dirname(__file__), "tasks", "queue.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
        except Exception:
            pass
    return list(_DEFAULT_QUEUE)
