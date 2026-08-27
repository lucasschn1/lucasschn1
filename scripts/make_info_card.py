#!/usr/bin/env python3
"""
make_info_card.py

Hand-authors a neofetch-style SVG panel: title bar, then colored key/value
rows (OS, Role, IDE, Languages, Hobbies, Contact, GitHub Stats). Each line
fades + slides in on a short stagger, like it's printing next to the
portrait. Content comes from data/profile_config.yaml so it can be edited
without touching this file.

Live numbers (repos, stars, followers, contributions) come from
data/github_stats.json and data/contributions.json when present (written
by fetch_github_stats.py / fetch_contributions.py); otherwise placeholders
are shown so the card still renders.

Set STATIC=1 to emit a frozen (already-fully-drawn) frame, handy for local
Quick Look previews.

Output: assets/info-card.svg
"""

import html
import json
import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, "data", "profile_config.yaml")
STATS_PATH = os.path.join(ROOT, "data", "github_stats.json")
CONTRIB_PATH = os.path.join(ROOT, "data", "contributions.json")
OUT_PATH = os.path.join(ROOT, "assets", "info-card.svg")

STATIC = os.environ.get("STATIC") == "1"

# ---- look & feel --------------------------------------------------------
FONT_FAMILY = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
FONT_SIZE = 13
LINE_H = FONT_SIZE * 1.55
CHAR_W = FONT_SIZE * 0.6
PAD_X = 18
PAD_Y = 18

PANEL_BG = "#0d1117"
PANEL_BORDER = "#30363d"
COLOR_HEADER = "#39d353"   # username@github + section headers
COLOR_LABEL = "#7d8590"    # key labels + dot leaders
COLOR_VALUE = "#c9d1d9"    # values
COLOR_RULE = "#30363d"

LABEL_COL = 24  # target character column where dot leaders end (mockup style)

STAGGER = 0.05
FADE_DUR = 0.35


def kv(label, value, col=LABEL_COL):
    prefix = f"{label}: "
    if len(prefix) >= col:
        dots = " "
    else:
        dots = "." * (col - len(prefix))
    return f"{prefix}{dots} {value}"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def build_lines(cfg):
    """Returns a list of (kind, text) tuples. kind: 'header' | 'rule' | 'kv' | 'blank'"""
    stats = load_json(STATS_PATH)
    contrib = load_json(CONTRIB_PATH)

    repos = stats.get("public_repos", "…")
    stars = stats.get("total_stars", "…")
    followers = stats.get("followers", "…")
    contributions_1y = contrib.get("total_contributions", stats.get("contributions_last_year", "…"))

    lines = []
    lines.append(("header", f"{cfg['username']}@github"))
    lines.append(("rule", None))

    lines.append(("kv", kv("OS", cfg["os"])))
    lines.append(("kv", kv("Role", cfg["role"])))
    lines.append(("kv", kv("IDE", cfg["ide"])))
    lines.append(("blank", None))

    lines.append(("kv", kv("Languages.Programming", ", ".join(cfg["languages_programming"]))))
    lines.append(("kv", kv("Languages.Spoken", ", ".join(cfg["languages_spoken"]))))
    lines.append(("blank", None))

    lines.append(("kv", kv("Hobbies.Tech", ", ".join(cfg["hobbies_tech"]))))
    lines.append(("kv", kv("Hobbies.Life", ", ".join(cfg["hobbies_life"]))))
    lines.append(("blank", None))

    lines.append(("header", "Contact"))
    contact = cfg["contact"]
    lines.append(("kv", kv("Email.Personal", contact["email"])))
    lines.append(("kv", kv("LinkedIn", f"/in/{contact['linkedin']}")))
    if contact.get("discord"):
        lines.append(("kv", kv("Discord", contact["discord"])))
    lines.append(("blank", None))

    lines.append(("header", "GitHub Stats"))
    lines.append(("kv", kv("Repos", str(repos), col=14) + f"    Stars: ...... {stars}"))
    lines.append(("kv", kv("Contributions (1y)", str(contributions_1y), col=22) + f"  Followers: .. {followers}"))

    return lines


def esc(s):
    return html.escape(s, quote=False)


def build_svg(lines):
    n = len(lines)
    max_chars = max((len(t) for k, t in lines if t), default=40)
    width = PAD_X * 2 + max_chars * CHAR_W
    height = PAD_Y * 2 + n * LINE_H

    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.1f}" height="{height:.1f}" '
        f'viewBox="0 0 {width:.1f} {height:.1f}" font-family="{FONT_FAMILY}">'
    )
    svg.append(
        f'<rect x="0.5" y="0.5" width="{width - 1:.1f}" height="{height - 1:.1f}" rx="10" '
        f'fill="{PANEL_BG}" stroke="{PANEL_BORDER}"/>'
    )
    svg.append(f'<style>text{{font-size:{FONT_SIZE}px;}}</style>')

    y = PAD_Y + FONT_SIZE
    row_i = 0
    for kind, text in lines:
        begin = row_i * STAGGER
        anim = "" if STATIC else (
            f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.3f}s" '
            f'dur="{FADE_DUR:.2f}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="-4 0" to="0 0" begin="{begin:.3f}s" dur="{FADE_DUR:.2f}s" fill="freeze"/>'
        )
        opacity_attr = "1" if STATIC else "0"

        if kind == "rule":
            rule_w = max_chars * CHAR_W
            svg.append(
                f'<line x1="{PAD_X}" y1="{y - FONT_SIZE * 0.4:.2f}" '
                f'x2="{PAD_X + rule_w:.2f}" y2="{y - FONT_SIZE * 0.4:.2f}" '
                f'stroke="{COLOR_RULE}"/>'
            )
            y += LINE_H * 0.6
            row_i += 1
            continue

        if kind == "blank":
            y += LINE_H * 0.55
            continue

        color = COLOR_HEADER if kind == "header" else COLOR_VALUE
        weight_attr = "font-weight='600'" if kind == "header" else ""
        svg.append(
            f'<g opacity="{opacity_attr}">{anim}'
            f'<text x="{PAD_X}" y="{y:.2f}" xml:space="preserve" fill="{color}" '
            f'{weight_attr}>{esc(text)}</text>'
            f'</g>'
        )
        y += LINE_H
        row_i += 1

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    cfg = load_config()
    lines = build_lines(cfg)
    svg = build_svg(lines)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(lines)} lines, static={STATIC})")


if __name__ == "__main__":
    main()
