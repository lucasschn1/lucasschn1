#!/usr/bin/env python3
"""
make_info_card.py

Content module for the whoami card: turns data/profile_config.yaml (+ the live
GitHub numbers when present) into neofetch-style lines that make_whoami_card.py
renders. No SVG is produced here.

Line kinds returned by build_lines():
  ('top', text)      -> "username@github ----------------------"
  ('section', text)  -> "- Contact ---------------------------"
  ('row', text)      -> ". Label: ............ value"  (right-aligned value)
  ('blank', None)
"""

import html
import json
import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, "data", "profile_config.yaml")
STATS_PATH = os.path.join(ROOT, "data", "github_stats.json")
CONTRIB_PATH = os.path.join(ROOT, "data", "contributions.json")

ROW_PREFIX = ". "
MIN_LEADERS = 2


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def esc(s):
    return html.escape(s, quote=False)


def _fmt(n):
    return f"{n:,}" if isinstance(n, int) else str(n)


def build_lines(cfg, stats=None, contrib=None):
    stats = stats if stats is not None else load_json(STATS_PATH)
    contrib = contrib if contrib is not None else load_json(CONTRIB_PATH)

    def joined(key):
        return ", ".join(cfg.get(key, []))

    # (section_title_or_None, [(label, value), ...])
    groups = []

    sysinfo = [("OS", cfg["os"])]
    if cfg.get("host"):
        sysinfo.append(("Host", cfg["host"]))
    if cfg.get("title"):
        sysinfo.append(("Kernel", cfg["title"]))
    sysinfo.append(("IDE", cfg["ide"]))
    groups.append((None, sysinfo))

    langs = [("Languages.Programming", joined("languages_programming"))]
    if cfg.get("languages_computer"):
        langs.append(("Languages.Computer", joined("languages_computer")))
    langs.append(("Languages.Real", joined("languages_spoken")))
    groups.append((None, langs))

    groups.append((None, [
        ("Hobbies.Tech", joined("hobbies_tech")),
        ("Hobbies.Life", joined("hobbies_life")),
    ]))

    contact = cfg["contact"]
    crows = [
        ("Email.Personal", contact["email"]),
        ("LinkedIn", f"/in/{contact['linkedin']}/"),
    ]
    if contact.get("discord"):
        crows.append(("Discord", contact["discord"]))
    groups.append(("Contact", crows))

    repos = _fmt(stats.get("public_repos", "-"))
    commits = _fmt(stats.get("total_commits", "-"))
    contribs = _fmt(contrib.get("total_contributions", "-"))
    active = _fmt(contrib.get("active_days", "-"))

    pr = stats.get("pull_requests") or {}
    pr_open, pr_merged = pr.get("opened"), pr.get("merged")
    if pr_open is not None and pr_merged is not None:
        prs = f"{_fmt(pr_open)} ({_fmt(pr_merged)} merged)"
    else:
        prs = _fmt(pr_open if pr_open is not None else "-")

    # ---- width: widest "prefix + label + ': ' + ' ' + value" + min leaders ----
    width = 0
    for _, rows in groups:
        for label, value in rows:
            base = f"{ROW_PREFIX}{label}: "
            width = max(width, len(base) + 1 + len(str(value)) + MIN_LEADERS)
    top = f"{cfg['username']}@github "
    width = max(width, len(top) + 8)

    def one(label, value):
        base = f"{ROW_PREFIX}{label}: "
        tail = f" {value}"
        dots = width - len(base) - len(tail)
        return base + ("." * dots if dots >= 1 else " ") + tail

    def two(l1, v1, l2, v2):
        a, a_tail = f"{ROW_PREFIX}{l1}: ", f" {v1}"
        b, b_tail = f"  |  {l2}: ", f" {v2}"
        slack = width - (len(a) + len(a_tail) + len(b) + len(b_tail))
        d1 = max(1, slack // 2)
        d2 = max(1, slack - d1)
        return a + "." * d1 + a_tail + b + "." * d2 + b_tail

    out = [("top", top + "-" * (width - len(top)))]
    for title, rows in groups:
        out.append(("blank", None))
        if title:
            head = f"- {title} "
            out.append(("section", head + "-" * (width - len(head))))
        for label, value in rows:
            out.append(("row", one(label, value)))

    out.append(("blank", None))
    head = "- GitHub Stats "
    out.append(("section", head + "-" * (width - len(head))))
    out.append(("row", two("Repos", repos, "PRs", prs)))
    out.append(("row", two("Commits", commits, "Active days (1y)", active)))
    out.append(("row", one("Contributions (1y)", contribs)))

    loc = stats.get("lines_of_code")
    if loc:
        val = (f"{_fmt(loc['net'])} ( {_fmt(loc['added'])}++, "
               f"{_fmt(loc['removed'])}-- )")
        out.append(("row", one("Lines of Code on GitHub", val)))
    return out
