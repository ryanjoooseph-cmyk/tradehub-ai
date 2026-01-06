from __future__ import annotations
import os
from typing import Dict, Any, List
from openai import OpenAI

def _fallback_files(task: Dict[str, Any]) -> List[Dict[str, str]]:
    feature = str(task.get("feature") or "task")
    content = f"# {feature}\n\nThis file was generated without OpenAI because OPENAI_API_KEY was not set.\n"
    return [{"path": f"agents/{feature}/plan.md", "content": content}]

def build_files(task: Dict[str, Any]) -> List[Dict[str, str]]:
    key = os.environ.get("OPENAI_API_KEY")
    model = os.environ.get("OPENAI_MODEL","gpt-4o-mini")
    feature = str(task.get("feature") or "task")
    route = str(task.get("route") or "/")
    notes = str(task.get("notes") or "")
    if not key:
        return _fallback_files(task)
    client = OpenAI(api_key=key)
    prompt = f"Create a concise implementation plan for building the UI and API for feature '{feature}' targeting route '{route}'. Output markdown only with concrete file paths and brief responsibilities. Keep under 200 lines. Notes: {notes}"
    resp = client.chat.completions.create(model=model,messages=[{"role":"system","content":"You generate code plans."},{"role":"user","content":prompt}],temperature=0.2)
    text = resp.choices[0].message.content if resp and resp.choices else "Plan unavailable."
    return [{"path": f"agents/{feature}/plan.md", "content": text}]
