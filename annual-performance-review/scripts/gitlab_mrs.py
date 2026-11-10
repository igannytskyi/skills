#!/usr/bin/env python3
"""Collect a person's GitLab merge requests for a review period.

Sources (combine freely):
  --group PATH      every project in a group and its subgroups (repeatable)
  --project PATH    a single project, e.g. a private personal repo (repeatable)
  --all-visible     every project the token can see, incl. your private repos

Roles: author (MRs they wrote), reviewer (MRs they were asked to review), or both.

Auth: GITLAB_TOKEN env var (scope read_api), else `glab auth token`/glab config.
Host: --host or GITLAB_HOST env var, default gitlab.com (self-hosted works too).
The token is only sent to the chosen host and never printed.

Examples:
  GITLAB_TOKEN=... python3 -I gitlab_mrs.py --group my-company/backend --since 2026-01-01
  python3 -I gitlab_mrs.py --all-visible --author jdoe --role both --format json
  python3 -I gitlab_mrs.py --host gitlab.example.com --group platform --project jdoe/side-tool
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone


def get_token(host):
    for var in ("GITLAB_TOKEN", "GITLAB_PRIVATE_TOKEN", "GL_TOKEN"):
        if os.environ.get(var):
            return os.environ[var]
    if shutil.which("glab"):
        for cmd in (["glab", "config", "get", "token", "--host", host],
                    ["glab", "auth", "token", "--hostname", host]):
            try:
                out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                tok = out.stdout.strip()
                if out.returncode == 0 and tok:
                    return tok
            except Exception:
                pass
    return None


class GitLab:
    def __init__(self, host, token):
        self.base = f"https://{host}/api/v4"
        self.token = token

    def get(self, path, params=None):
        """GET with pagination; returns a list (or a dict for single objects)."""
        params = dict(params or {})
        params.setdefault("per_page", 100)
        page, results = 1, []
        while True:
            params["page"] = page
            url = f"{self.base}/{path}?{urllib.parse.urlencode(params, doseq=True)}"
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            if self.token:
                req.add_header("PRIVATE-TOKEN", self.token)
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.load(resp)
                    next_page = resp.headers.get("X-Next-Page")
            except urllib.error.HTTPError as e:
                body = e.read().decode(errors="replace")[:300]
                raise SystemExit(f"GitLab API error {e.code} on {path}: {body}")
            if not isinstance(data, list):
                return data
            results.extend(data)
            if not next_page:
                return results
            page = int(next_page)


def enc(path):
    return urllib.parse.quote(path, safe="")


def parse_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--host", default=os.environ.get("GITLAB_HOST", "gitlab.com"))
    p.add_argument("--author", help="GitLab username; default: the token's own user")
    p.add_argument("--group", action="append", default=[], help="group path, e.g. company/backend")
    p.add_argument("--project", action="append", default=[], help="project path, e.g. me/private-repo")
    p.add_argument("--all-visible", action="store_true", help="all projects the token can see")
    p.add_argument("--role", choices=["author", "reviewer", "both"], default="author")
    p.add_argument("--state", choices=["merged", "all"], default="merged")
    p.add_argument("--since", default=f"{date.today().year}-01-01", help="YYYY-MM-DD")
    p.add_argument("--until", default=date.today().isoformat(), help="YYYY-MM-DD")
    p.add_argument("--format", choices=["md", "json"], default="md")
    p.add_argument("--desc-chars", type=int, default=300, help="description excerpt length (json)")
    a = p.parse_args()

    if not (a.group or a.project or a.all_visible):
        p.error("give at least one of --group, --project, --all-visible")

    host = a.host.replace("https://", "").replace("http://", "").rstrip("/")
    token = get_token(host)
    gl = GitLab(host, token)
    if not token:
        print("warning: no token (set GITLAB_TOKEN with read_api); only public data is visible",
              file=sys.stderr)

    user = a.author
    if not user:
        if not token:
            p.error("--author is required without a token")
        user = gl.get("user")["username"]

    since = datetime.fromisoformat(a.since).replace(tzinfo=timezone.utc)
    until = datetime.fromisoformat(a.until).replace(hour=23, minute=59, second=59, tzinfo=timezone.utc)

    sources = [(f"groups/{enc(g)}/merge_requests", {}) for g in a.group]
    sources += [(f"projects/{enc(pr)}/merge_requests", {}) for pr in a.project]
    if a.all_visible:
        sources.append(("merge_requests", {"scope": "all"}))

    roles = ["author", "reviewer"] if a.role == "both" else [a.role]
    found = {}
    for path, extra in sources:
        for role in roles:
            params = dict(extra)
            params["author_username" if role == "author" else "reviewer_username"] = user
            params["updated_after"] = since.isoformat()  # cheap server-side prefilter
            if a.state == "merged":
                params["state"] = "merged"
            for mr in gl.get(path, params):
                key = mr["id"]
                if key in found:
                    found[key]["roles"].add(role)
                    continue
                ts = parse_dt(mr.get("merged_at")) if a.state == "merged" else parse_dt(mr.get("created_at"))
                if not ts or not (since <= ts <= until):
                    continue
                mr["roles"] = {role}
                found[key] = mr

    projects = {}
    def project_path(mr):
        ref = (mr.get("references") or {}).get("full", "")
        if "!" in ref:
            return ref.rsplit("!", 1)[0]
        pid = mr["project_id"]
        if pid not in projects:
            projects[pid] = gl.get(f"projects/{pid}").get("path_with_namespace", str(pid))
        return projects[pid]

    rows = []
    for mr in found.values():
        rows.append({
            "project": project_path(mr),
            "iid": mr["iid"],
            "title": mr["title"],
            "roles": sorted(mr["roles"]),
            "state": mr["state"],
            "created_at": mr.get("created_at"),
            "merged_at": mr.get("merged_at"),
            "labels": mr.get("labels", []),
            "milestone": (mr.get("milestone") or {}).get("title"),
            "comments": mr.get("user_notes_count"),
            "url": mr["web_url"],
            "description": (mr.get("description") or "").strip()[: a.desc_chars],
        })
    rows.sort(key=lambda r: r["merged_at"] or r["created_at"] or "")

    if a.format == "json":
        json.dump({"host": host, "user": user, "since": a.since, "until": a.until,
                   "count": len(rows), "merge_requests": rows}, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return

    by_proj = {}
    for r in rows:
        by_proj[r["project"]] = by_proj.get(r["project"], 0) + 1
    print(f"# GitLab MRs: {user} @ {host}, {a.since} .. {a.until}\n")
    print(f"Total: {len(rows)} ({', '.join(roles)}); projects: {len(by_proj)}\n")
    for proj, n in sorted(by_proj.items(), key=lambda x: -x[1]):
        print(f"- {proj}: {n}")
    print("\n| Date | Project | MR | Title | Role | Labels |\n|---|---|---|---|---|---|")
    for r in rows:
        d = (r["merged_at"] or r["created_at"] or "")[:10]
        title = r["title"].replace("|", "\\|")
        print(f"| {d} | {r['project']} | [!{r['iid']}]({r['url']}) | {title} | "
              f"{'/'.join(r['roles'])} | {', '.join(r['labels'][:4])} |")


if __name__ == "__main__":
    main()
