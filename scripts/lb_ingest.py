#!/usr/bin/env python3
"""Ingest the conjecture repos into the LivingBrain memory, incrementally.

For every submodule listed in .gitmodules (plus this superproject) it captures, from the
remote's default branch:

* documentation: README.md, AGENTS.md, docs/*.md, paper/README.md, whenever a file's content
  changes;
* the history of attempts: commit messages not yet ingested, as one note per repo per run;
* pull requests (all states): title, state, body, and review summary, re-captured when updated;
* unmerged branches: name and recent commit subjects, i.e. attempts in flight or abandoned.

Each capture's ``originRef`` carries the commit / content hash / update time, so LivingBrain
deduplicates replays; a local state file avoids sending what was already sent.

Credentials come from the ``livingbrain`` entry of ~/.claude.json and are never printed.

Usage:
    scripts/lb_ingest.py [--dry-run] [--repo NAME] [--state PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

BRAIN_ID = os.environ.get("LB_BRAIN_ID", "63af7dac-de64-581f-9949-9e1bed98d7fd")
SOURCE = {"channel": "claude-code", "label": "RH formalization repos", "ref": "conjectures/lb_ingest"}
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STATE = Path.home() / ".local/state/conjectures-lb-ingest.json"
DOC_GLOBS = ["README.md", "AGENTS.md", "docs/*.md", "paper/README.md"]
MAX_DOC = 60_000
OWNER = "senamakel"


# --------------------------------------------------------------------------- LivingBrain client
class LivingBrain:
    def __init__(self) -> None:
        cfg = json.loads((Path.home() / ".claude.json").read_text())["mcpServers"]["livingbrain"]
        self.url = cfg["url"]
        self.headers = dict(cfg.get("headers", {}))
        self.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "conjectures-lb-ingest/1.0",
        })
        self.sid: str | None = None
        self._id = 0

    def _post(self, body: dict) -> list[dict]:
        headers = dict(self.headers)
        if self.sid:
            headers["mcp-session-id"] = self.sid
        req = urllib.request.Request(self.url, json.dumps(body).encode(), headers, method="POST")
        with urllib.request.urlopen(req, timeout=300) as resp:
            self.sid = resp.headers.get("mcp-session-id") or self.sid
            raw = resp.read().decode()
        if raw.lstrip().startswith("{"):
            return [json.loads(raw)]
        return [json.loads(l[5:]) for l in raw.splitlines() if l.startswith("data:") and l[5:].strip()]

    def connect(self) -> None:
        self._post({"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {},
            "clientInfo": {"name": "conjectures-lb-ingest", "version": "1.0"}}})
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def call(self, name: str, arguments: dict) -> dict:
        self._id += 1
        msgs = self._post({"jsonrpc": "2.0", "id": self._id, "method": "tools/call",
                           "params": {"name": name, "arguments": arguments}})
        res = next((m for m in msgs if m.get("id") == self._id), msgs[-1] if msgs else {})
        if "error" in res:
            raise RuntimeError(f"{name}: {res['error']}")
        result = res.get("result", {})
        if result.get("isError"):
            raise RuntimeError(f"{name}: {result.get('content')}")
        text = (result.get("content") or [{}])[0].get("text", "")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"text": text}


# --------------------------------------------------------------------------- helpers
def sh(*args: str, cwd: Path | None = None, check: bool = True) -> str:
    out = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and out.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}: {out.stderr.strip()}")
    return out.stdout


def h(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def submodules() -> list[str]:
    out = sh("git", "config", "-f", ".gitmodules", "--get-regexp", r"submodule\..*\.path", cwd=ROOT)
    return [line.split()[1] for line in out.splitlines()]


def remote_slug(path: Path) -> str:
    url = sh("git", "remote", "get-url", "origin", cwd=path).strip()
    slug = url.rstrip("/").removesuffix(".git").split("github.com")[-1].lstrip(":/")
    return slug


def capture(label: str, origin: str, content: str, bucket: str = "projects") -> dict:
    return {"kind": "note", "bucket": bucket, "label": label, "originRef": origin,
            "content": content, "source": SOURCE}


# --------------------------------------------------------------------------- collectors
def collect_repo(name: str, path: Path, state: dict) -> list[dict]:
    slug = remote_slug(path)
    repo = slug.split("/")[-1]
    st = state.setdefault(slug, {})
    fetch = ["git", "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*"]
    if sh("git", "rev-parse", "--is-shallow-repository", cwd=path).strip() == "true":
        fetch.insert(3, "--unshallow")  # the history of attempts needs every commit
    sh(*fetch, cwd=path)
    head_ref = sh("git", "symbolic-ref", "-q", "--short", "refs/remotes/origin/HEAD", cwd=path, check=False).strip() or "origin/main"
    head = sh("git", "rev-parse", head_ref, cwd=path).strip()
    items: list[dict] = []

    # Documentation, re-captured when its content changes.
    docs = st.setdefault("docs", {})
    files = sh("git", "ls-tree", "-r", "--name-only", head, cwd=path).splitlines()
    import fnmatch
    for f in files:
        if not any(fnmatch.fnmatch(f, g) for g in DOC_GLOBS):
            continue
        text = sh("git", "show", f"{head}:{f}", cwd=path)
        digest = h(text)
        if docs.get(f) == digest:
            continue
        body = text if len(text) <= MAX_DOC else text[:MAX_DOC] + "\n\n[truncated]"
        items.append(capture(
            f"{repo}: {f} @ {head[:7]}",
            f"https://github.com/{slug}/blob/{head}/{f}#{digest}",
            f"Repository {slug}, file {f}, at commit {head[:10]} (default branch).\n\n{body}"))
        docs[f] = digest

    # Commit history: the sequence of attempts, newest last.
    last = st.get("last_commit")
    known = last and sh("git", "cat-file", "-t", last, cwd=path, check=False).strip() == "commit"
    rng = f"{last}..{head}" if known else head
    if not known and last:
        note = (f"Note: the previously ingested commit {last[:10]} is no longer on the remote; "
                "the default branch history was rewritten, so this is the full history again.\n\n")
    else:
        note = ""
    log = sh("git", "log", "--reverse", "--date=short",
             "--format=### %h %ad %s%n%b", rng, cwd=path).strip()
    if log:
        items.append(capture(
            f"{repo}: commit history {'' if not known else last[:7] + '..'}{head[:7]}",
            f"git:{slug}:{(last or 'root')[:12]}..{head[:12]}",
            f"Commit history of {slug} (default branch), oldest first, up to {head[:10]}. "
            f"Each commit is an attempt or step in the formalisation.\n\n{note}{log}"))
    st["last_commit"] = head

    # Unmerged branches: attempts in flight or abandoned.
    branches = []
    for ref in sh("git", "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin", cwd=path).split():
        if ref.endswith("/HEAD") or ref == head_ref:
            continue
        ahead = sh("git", "log", "--date=short", "--format=  - %h %ad %s", f"{head}..{ref}", cwd=path).strip()
        if ahead:
            branches.append(f"- `{ref.removeprefix('origin/')}` (not merged):\n{ahead}")
    if branches:
        text = "\n".join(branches)
        if st.get("branches") != h(text):
            items.append(capture(
                f"{repo}: unmerged branches",
                f"git:{slug}:branches#{h(text)}",
                f"Unmerged branches of {slug} as of {head[:10]}: work in flight or abandoned "
                f"attempts not on the default branch.\n\n{text}"))
            st["branches"] = h(text)

    # Pull requests, all states.
    prs = json.loads(sh("gh", "pr", "list", "-R", slug, "--state", "all", "--limit", "500", "--json",
                        "number,title,state,body,updatedAt,mergedAt,headRefName,url,reviews,comments"))
    seen = st.setdefault("prs", {})
    for pr in prs:
        key = str(pr["number"])
        if seen.get(key) == pr["updatedAt"]:
            continue
        reviews = "\n".join(f"- review by {r['author']['login']} ({r['state']}): {r['body'][:1500]}"
                            for r in pr.get("reviews", []) if r.get("body"))
        comments = "\n".join(f"- comment by {c['author']['login']}: {c['body'][:1500]}"
                             for c in pr.get("comments", []) if c.get("body"))
        outcome = "merged" if pr.get("mergedAt") else pr["state"].lower()
        if outcome == "closed":
            outcome = "closed without merging (abandoned attempt)"
        items.append(capture(
            f"{repo} PR #{pr['number']}: {pr['title']}",
            f"{pr['url']}#{pr['updatedAt']}",
            f"Pull request {slug}#{pr['number']} ({outcome}), branch `{pr['headRefName']}`: "
            f"{pr['title']}\n\n{pr['body'] or '(no description)'}"
            + (f"\n\nReviews:\n{reviews}" if reviews else "")
            + (f"\n\nComments:\n{comments}" if comments else "")))
        seen[key] = pr["updatedAt"]
    return items


def collect_superproject(state: dict) -> list[dict]:
    st = state.setdefault("_superproject", {})
    items = []
    for f in ["AGENTS.md", "README.md"]:
        p = ROOT / f
        if not p.exists():
            continue
        text = p.read_text()
        digest = h(text)
        if st.get(f) == digest:
            continue
        items.append(capture(
            f"conjectures: {f}",
            f"https://github.com/{OWNER}/conjectures/blob/main/{f}#{digest}",
            f"The conjectures tracking superproject ({OWNER}/conjectures), {f}: the programme's "
            f"status checklist, proof-tier rules and README rules.\n\n{text}"))
        st[f] = digest
    return items


# --------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print what would be captured; send nothing")
    ap.add_argument("--repo", action="append", help="only this submodule (repeatable)")
    ap.add_argument("--state", type=Path, default=DEFAULT_STATE)
    args = ap.parse_args()

    state = json.loads(args.state.read_text()) if args.state.exists() else {}
    names = args.repo or submodules()
    items: list[dict] = [] if args.repo else collect_superproject(state)
    for name in names:
        path = ROOT / name
        if not (path / ".git").exists():
            print(f"skip {name}: not checked out", file=sys.stderr)
            continue
        try:
            items += collect_repo(name, path, state)
        except Exception as e:  # one repo failing must not stop the rest
            print(f"error {name}: {e}", file=sys.stderr)

    if args.dry_run:
        for it in items:
            print(f"- {it['label']}  [{len(it['content'])} chars]  {it['originRef']}")
        print(f"{len(items)} captures (dry run, nothing sent, state not saved)")
        return 0
    if not items:
        print("nothing new")
        return 0

    lb = LivingBrain()
    lb.connect()
    sent = 0
    for i in range(0, len(items), 50):
        chunk = items[i:i + 50]
        res = lb.call("captures_capture_batch", {"brainId": BRAIN_ID, "body": {"items": chunk}})
        sent += int(res.get("ingested", len(chunk))) if isinstance(res, dict) else len(chunk)
    args.state.parent.mkdir(parents=True, exist_ok=True)
    args.state.write_text(json.dumps(state, indent=1, sort_keys=True))
    print(f"sent {sent}/{len(items)} captures to LivingBrain")
    return 0


if __name__ == "__main__":
    sys.exit(main())
