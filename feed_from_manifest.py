#!/usr/bin/env python3
import json, os, sys

MANIFEST_PATH = os.environ.get("MANIFEST_PATH", "manifest.json")

def _normalize(obj):
    tasks = []
    if isinstance(obj, dict):
        if "tasks" in obj:
            return _normalize(obj["tasks"])
        feature = obj.get("feature") or obj.get("name") or obj.get("id") or str(obj)
        d = {k: v for k, v in obj.items() if k != "feature"}
        d["feature"] = feature
        tasks.append(d)
    elif isinstance(obj, list):
        for it in obj:
            if isinstance(it, dict):
                feature = it.get("feature") or it.get("name") or it.get("id") or str(it)
                d = {k: v for k, v in it.items() if k != "feature"}
                d["feature"] = feature
                tasks.append(d)
            elif isinstance(it, str):
                s = it.strip()
                if s:
                    tasks.append({"feature": s})
    elif isinstance(obj, str):
        for line in obj.splitlines():
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            try:
                tasks.extend(_normalize(json.loads(line)))
            except Exception:
                tasks.append({"feature": line})
    else:
        tasks.append({"feature": str(obj)})
    return tasks

def load_manifest(path):
    if not os.path.exists(path):
        print(f"[feed] manifest not found: {path} — nothing to seed.")
        return []
    raw = open(path, "r", encoding="utf-8").read()
    try:
        return _normalize(json.loads(raw))
    except json.JSONDecodeError:
        return _normalize(raw)

def main():
    tasks = load_manifest(MANIFEST_PATH)
    print(f"[feed] loaded {len(tasks)} task definitions")
    # Intentionally a no-op feeder (don’t crash the loop if seeding isn’t needed).
    # If you later wire Supabase inserts here, keep the try/except pattern.
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[feed] non-fatal: {e}")
        sys.exit(0)