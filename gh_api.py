from __future__ import annotations
import os, base64, requests
from typing import Optional

BASE = "https://api.github.com"

def _hdr():
    t = os.environ.get("GITHUB_TOKEN")
    return {"Authorization": f"token {t}", "Accept": "application/vnd.github+json"}

def get_repo_default_branch(repo: str) -> Optional[str]:
    r = requests.get(f"{BASE}/repos/{repo}", headers=_hdr(), timeout=30)
    if r.status_code == 200:
        return r.json().get("default_branch")
    return None

def get_ref_sha(repo: str, ref: str) -> Optional[str]:
    r = requests.get(f"{BASE}/repos/{repo}/git/ref/heads/{ref}", headers=_hdr(), timeout=30)
    if r.status_code == 200:
        return r.json().get("object",{}).get("sha")
    return None

def create_branch(repo: str, new_branch: str, from_sha: str) -> bool:
    p = {"ref": f"refs/heads/{new_branch}", "sha": from_sha}
    r = requests.post(f"{BASE}/repos/{repo}/git/refs", headers=_hdr(), json=p, timeout=30)
    return r.status_code in (201,422)

def get_file_sha(repo: str, path: str, branch: str) -> Optional[str]:
    r = requests.get(f"{BASE}/repos/{repo}/contents/{path}", headers=_hdr(), params={"ref": branch}, timeout=30)
    if r.status_code == 200:
        return r.json().get("sha")
    return None

def put_file(repo: str, path: str, content_str: str, message: str, branch: str, sha: Optional[str]) -> bool:
    body = {"message": message, "content": base64.b64encode(content_str.encode("utf-8")).decode("ascii"), "branch": branch}
    if sha:
        body["sha"] = sha
    r = requests.put(f"{BASE}/repos/{repo}/contents/{path}", headers=_hdr(), json=body, timeout=60)
    return r.status_code in (200,201)

def create_pr(repo: str, title: str, head: str, base: str, body: str) -> Optional[str]:
    r = requests.post(f"{BASE}/repos/{repo}/pulls", headers=_hdr(), json={"title": title, "head": head, "base": base, "body": body}, timeout=30)
    if r.status_code in (201,200):
        return r.json().get("html_url")
    return None
