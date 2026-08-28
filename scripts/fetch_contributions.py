#!/usr/bin/env python3
"""
fetch_contributions.py

No GitHub token needed. GitHub serves each user's contribution calendar as
public HTML at https://github.com/users/<username>/contributions -- the
same fragment the profile page itself loads. We fetch it with `requests`,
parse the day cells with BeautifulSoup, and write data/contributions.json
with the raw days plus a few derived stats (current streak, longest streak,
best day, monthly totals).

Caveat: this depends on GitHub's current markup for that page (table cells
with data-date / data-level, and <tool-tip> elements carrying the exact
count). If GitHub changes that markup, the selectors below may need a
small update -- the script degrades gracefully (counts become null, level
is still used to color the heatmap) rather than crashing silently.
"""

import datetime
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GITHUB_USERNAME", "lucasschn1")
URL = f"https://github.com/users/{USERNAME}/contributions"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "data", "contributions.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; profile-readme-bot/1.0; "
                  "+https://github.com/{}/{})".format(USERNAME, USERNAME)
}


def fetch_html():
    resp = requests.get(URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse_total_contributions(soup, days):
    text = soup.get_text(" ", strip=True)
    m = re.search(r"([\d,]+)\s+contributions?\s+in the last year", text, re.IGNORECASE)
    if m:
        return int(m.group(1).replace(",", ""))
    # fall back to summing per-day counts if we have them
    counted = [d["count"] for d in days if d["count"] is not None]
    if counted:
        return sum(counted)
    return None


def parse_tooltip_counts(soup):
    """Map an element id -> contribution count, parsed from <tool-tip> /
    legacy [data-hovercard-type] text like "3 contributions on May 24th."
    """
    counts_by_id = {}
    for tip in soup.select("tool-tip, .sr-only, [data-testid='contribution-tooltip']"):
        target = tip.get("for") or tip.get("data-target")
        text = tip.get_text(" ", strip=True)
        if not target or not text:
            continue
        m = re.match(r"(No|\d[\d,]*)\s+contributions?\s+on", text, re.IGNORECASE)
        if not m:
            continue
        raw = m.group(1)
        count = 0 if raw.lower() == "no" else int(raw.replace(",", ""))
        counts_by_id[target] = count
    return counts_by_id


def parse_days(soup):
    cells = soup.select("td.ContributionCalendar-day[data-date], td[data-date][data-level]")
    if not cells:
        # last-resort fallback selector in case class names changed
        cells = soup.select("[data-date][data-level]")

    if not cells:
        print("warning: no contribution day cells found -- GitHub's markup "
              "may have changed; writing an empty calendar.", file=sys.stderr)
        return []

    tooltip_counts = parse_tooltip_counts(soup)

    days = []
    for cell in cells:
        date = cell.get("data-date")
        level_raw = cell.get("data-level")
        level = int(level_raw) if level_raw is not None and level_raw.isdigit() else 0
        cell_id = cell.get("id")
        count = tooltip_counts.get(cell_id)
        days.append({"date": date, "level": level, "count": count})

    days.sort(key=lambda d: d["date"])
    return days


def compute_streaks(days):
    current_streak = 0
    longest_streak = 0
    running = 0
    today = datetime.date.today().isoformat()

    for d in days:
        active = (d["count"] or 0) > 0 if d["count"] is not None else d["level"] > 0
        if active:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 0

    # current streak = trailing run of active days up to the most recent day we have
    for d in reversed(days):
        active = (d["count"] or 0) > 0 if d["count"] is not None else d["level"] > 0
        if active:
            current_streak += 1
        else:
            break

    return current_streak, longest_streak


def count_active_days(days):
    return sum(
        1 for d in days
        if ((d["count"] or 0) > 0 if d["count"] is not None else d["level"] > 0)
    )


def compute_best_day(days):
    scored = [d for d in days if d["count"] is not None]
    if not scored:
        return None
    best = max(scored, key=lambda d: d["count"])
    return {"date": best["date"], "count": best["count"]}


def compute_monthly_totals(days):
    totals = {}
    for d in days:
        if not d["date"]:
            continue
        month = d["date"][:7]  # YYYY-MM
        totals[month] = totals.get(month, 0) + (d["count"] or 0)
    return totals


def main():
    html_text = fetch_html()
    soup = BeautifulSoup(html_text, "html.parser")

    days = parse_days(soup)
    total = parse_total_contributions(soup, days)
    current_streak, longest_streak = compute_streaks(days)
    best_day = compute_best_day(days)
    monthly_totals = compute_monthly_totals(days)

    data = {
        "username": USERNAME,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_contributions": total,
        "active_days": count_active_days(days),
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "monthly_totals": monthly_totals,
        "days": days,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"wrote {OUT_PATH}: {len(days)} days, total={total}, "
          f"current_streak={current_streak}, longest_streak={longest_streak}")


if __name__ == "__main__":
    main()
