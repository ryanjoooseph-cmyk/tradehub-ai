from __future__ import annotations
from typing import List, Dict, Optional
from gh_api import get_repo_default_branch, get_ref_sha, create_branch, get_file_sha, put_file, create_pr

def open_pr_with_files(repo: str, base_branch: str, branch_name: str, files: List[Dict[str,str]], title: str, body: str) -> Optional[str]:
    base_sha = get_ref_sha(repo, base_branch)
    if not base_sha:
        return None
    ok = create_branch(repo, branch_name, base_sha)
    if not ok:
        return None
    for f in files:
        path = f["path"]
        content = f["content"]
        sha = get_file_sha(repo, path, branch_name)
        msg = f"add {path}"
        if not put_file(repo, path, content, msg, branch_name, sha):
            return None
    return create_pr(repo, title, head=branch_name, base=base_branch, body=body)
