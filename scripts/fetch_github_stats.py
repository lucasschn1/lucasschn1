#!/usr/bin/env python3
"""
fetch_github_stats.py

Public, unauthenticated GitHub REST API (60 req/hr per IP -- plenty for a
daily cron; a GITHUB_TOKEN, if present, just raises the limit):

  GET /users/{username}         -> public_repos, followers, following, created_at
  GET /users/{username}/repos   -> paginated, summed for total stars
  GET /search/commits?q=author  -> approximate total commit count

Writes data/github_stats.json, consumed by make_info_card.py for the
"GitHub Stats" section of the whoami card.
"""

import datetime
import json
import os
import time

import requests

USERNAME = os.environ.get("GITHUB_USERNAME", "lucasschn1")
API = "https://api.github.com"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "data", "github_stats.json")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": f"profile-readme-bot/1.0 (+https://github.com/{USERNAME}/{USERNAME})",
}
if os.environ.get("GITHUB_TOKEN"):
    HEADERS["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"


def get_json(path, **params):
    resp = requests.get(f"{API}{path}", headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def owned_repos():
    repos, page = [], 1
    while True:
        batch = get_json(f"/users/{USERNAME}/repos", per_page=100, page=page, type="owner")
        if not batch:
            break
        repos += batch
        if len(batch) < 100:
            break
        page += 1
    return repos


def lines_of_code(repos):
    """Sum the user's additions/deletions across their own repos via the
    per-repo contributor stats endpoint (may 202 while GitHub computes it)."""
    added = removed = 0
    got_any = False
    for repo in repos:
        if repo.get("fork"):
            continue
        url = f"{API}/repos/{USERNAME}/{repo['name']}/stats/contributors"
        for attempt in range(3):
            resp = requests.get(url, headers=HEADERS, timeout=30)
            if resp.status_code == 202:
                time.sleep(2)
                continue
            resp.raise_for_status()
            data = resp.json() or []
            for c in data:
                if (c.get("author") or {}).get("login") == USERNAME:
                    for w in c.get("weeks", []):
                        added += w.get("a", 0)
                        removed += w.get("d", 0)
                    got_any = True
            break
    if not got_any:
        return None
    return {"added": added, "removed": removed, "net": added - removed}


def total_commits():
    try:
        headers = dict(HEADERS, Accept="application/vnd.github.cloak-preview+json")
        resp = requests.get(
            f"{API}/search/commits",
            headers=headers,
            params={"q": f"author:{USERNAME}", "per_page": 1},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("total_count")
    except requests.RequestException:
        return None


def _search_issues_count(query):
    try:
        resp = requests.get(
            f"{API}/search/issues",
            headers=HEADERS,
            params={"q": query, "per_page": 1},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json().get("total_count")
    except requests.RequestException:
        return None


def pull_requests():
    return {
        "opened": _search_issues_count(f"author:{USERNAME} type:pr"),
        "merged": _search_issues_count(f"author:{USERNAME} type:pr is:merged"),
    }


def main():
    user = get_json(f"/users/{USERNAME}")
    repos = owned_repos()
    data = {
        "username": USERNAME,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "public_repos": user.get("public_repos"),
        "followers": user.get("followers"),
        "following": user.get("following"),
        "created_at": user.get("created_at"),
        "total_stars": sum(r.get("stargazers_count", 0) for r in repos),
        "total_commits": total_commits(),
        "pull_requests": pull_requests(),
        "lines_of_code": lines_of_code(repos),
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"wrote {OUT_PATH}: repos={data['public_repos']} stars={data['total_stars']} "
          f"commits={data['total_commits']} followers={data['followers']} "
          f"loc={data['lines_of_code']}")


if __name__ == "__main__":
    main()
