import os, json, tempfile, subprocess, pathlib, difflib
from typing import List, Dict, Any

def _ensure_dir(path: str):
    pathlib.Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)

def _write_file(path: str, content: str):
    _ensure_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def _append_file(path: str, content: str):
    _ensure_dir(path)
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)

def _delete_file(path: str):
    if os.path.exists(path):
        os.remove(path)

def _git(*args, cwd: str):
    return subprocess.check_output(["git", *args], cwd=cwd, text=True)

def _apply_items_to_dir(root: str, items: List[Dict[str, Any]]):
    for it in items:
        fp = os.path.join(root, it["file_path"])
        op = it["operation"]
        if op == "write":
            _write_file(fp, it.get("content",""))
        elif op == "append":
            _append_file(fp, it.get("content",""))
        elif op == "delete":
            _delete_file(fp)
        else:
            raise ValueError(f"Unknown operation: {op}")

def _diff_dir(cwd: str) -> str:
    try:
        return _git("diff", "--staged", cwd=cwd)
    except subprocess.CalledProcessError:
        # fallback: unstaged diff
        return _git("diff", cwd=cwd)

def apply_and_diff(diff_items: List[Dict[str,Any]],
                   github_token: str = None,
                   target_repo: str = None,
                   git_name: str = None,
                   git_email: str = None) -> dict:
    """
    If GitHub creds provided, clone repo, apply, git add, produce diff, and optionally commit/push.
    If not, apply to a temp dir and produce a synthetic diff (non-git).
    Returns: {"diff_text": str, "committed": bool}
    """
    # No repo flow: temp workspace diff
    if not (github_token and target_repo):
        # synthetic diff (before/after) for reviewer
        tmp = tempfile.TemporaryDirectory()
        root = tmp.name
        # produce "before" snapshot map
        before = {}
        for it in diff_items:
            p = os.path.join(root, it["file_path"])
            try:
                with open(p, "r", encoding="utf-8") as f:
                    before[it["file_path"]] = f.read().splitlines(keepends=False)
            except FileNotFoundError:
                before[it["file_path"]] = []
        # apply changes
        _apply_items_to_dir(root, diff_items)
        # after snapshot and diffs
        parts = []
        for it in diff_items:
            p = os.path.join(root, it["file_path"])
            after_lines = []
            if it["operation"] != "delete" and os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    after_lines = f.read().splitlines(keepends=False)
            diff_lines = difflib.unified_diff(
                before[it["file_path"]],
                after_lines,
                fromfile=f"a/{it['file_path']}",
                tofile=f"b/{it['file_path']}",
                lineterm=""
            )
            parts.append("\n".join(diff_lines))
        return {"diff_text": "\n".join(parts), "committed": False}

    # Repo flow: clone, apply, git add, create real diff
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_url = f"https://{github_token}:x-oauth-basic@github.com/{target_repo}.git"
        subprocess.check_call(["git", "clone", repo_url, tmpdir])
        if git_name and git_email:
            subprocess.check_call(["git", "-C", tmpdir, "config", "user.name", git_name])
            subprocess.check_call(["git", "-C", tmpdir, "config", "user.email", git_email])

        _apply_items_to_dir(tmpdir, diff_items)
        subprocess.check_call(["git", "-C", tmpdir, "add", "."], stdout=subprocess.DEVNULL)

        # produce a staged diff for reviewer
        diff_text = _git("diff", "--staged", cwd=tmpdir)

        return {"diff_text": diff_text, "committed": False}  # commit happens after reviewer approval

def commit_and_push(diff_items, github_token, target_repo, git_name, git_email, commit_msg="AI change"):
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_url = f"https://{github_token}:x-oauth-basic@github.com/{target_repo}.git"
        subprocess.check_call(["git", "clone", repo_url, tmpdir])
        if git_name and git_email:
            subprocess.check_call(["git", "-C", tmpdir, "config", "user.name", git_name])
            subprocess.check_call(["git", "-C", tmpdir, "config", "user.email", git_email])

        _apply_items_to_dir(tmpdir, diff_items)
        subprocess.check_call(["git", "-C", tmpdir, "add", "."], stdout=subprocess.DEVNULL)
        subprocess.check_call(["git", "-C", tmpdir, "commit", "-m", commit_msg])
        subprocess.check_call(["git", "-C", tmpdir, "push"])
