#!/usr/bin/env python3
"""
fetch_github_stats.py

No personal access token needed -- just the public, unauthenticated GitHub
REST API (rate-limited to 60 req/hour per IP, which is plenty for a
once-a-day cron):

  GET /users/{username}            -> public_repos, followers, following
  GET /users/{username}/repos      -> paginated list, summed for total stars

Writes data/github_stats.json, consumed by make_info_card.py for the
"GitHub Stats" section of the neofetch card.
"""

import datetime
import json
import os

import requests

USERNAME = os.environ.get("GITHUB_USERNAME", "lucasschn1")
API = "https://api.github.com"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "data", "github_stats.json")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": f"profile-readme-bot/1.0 (+https://github.com/{USERNAME}/{USERNAME})",
}
# GitHub Actions injects this automatically -- using it (instead of a
# manually-created personal access token) just raises the rate limit from
# 60/hr to 1000/hr. It is optional: the script works fine without it.
if os.environ.get("GITHUB_TOKEN"):
    HEADERS["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"


def get_user():
    resp = requests.get(f"{API}/users/{USERNAME}", headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_total_stars_and_top_repo():
    total_stars = 0
    top_repo = None
    page = 1
    while True:
        resp = requests.get(
            f"{API}/users/{USERNAME}/repos",
            headers=HEADERS,
            params={"per_page": 100, "page": page, "type": "owner"},
            timeout=30,
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        for repo in batch:
            stars = repo.get("stargazers_count", 0)
            total_stars += stars
            if top_repo is None or stars > top_repo["stars"]:
                top_repo = {"name": repo["name"], "stars": stars}
        if len(batch) < 100:
            break
        page += 1
    return total_stars, top_repo


def main():
    user = get_user()
    total_stars, top_repo = get_total_stars_and_top_repo()

    data = {
        "username": USERNAME,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "public_repos": user.get("public_repos"),
        "followers": user.get("followers"),
        "following": user.get("following"),
        "total_stars": total_stars,
        "top_repo": top_repo,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"wrote {OUT_PATH}: repos={data['public_repos']} stars={total_stars} "
          f"followers={data['followers']}")


if __name__ == "__main__":
    main()
