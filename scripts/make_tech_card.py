#!/usr/bin/env python3
"""
make_tech_card.py

Renders the tech stack as a minimal, borderless list: a muted label per group
followed by each tool's logo and name. Items wrap onto extra lines when a
group gets too wide.

The background is transparent and the file is written twice, once per theme
(assets/tech-card-dark.svg and assets/tech-card-light.svg). The README picks
one with <picture> + `prefers-color-scheme`, which GitHub resolves against the
theme chosen in GitHub's own settings -- a media query *inside* an SVG shown
through <img> only sees the OS/browser preference, so a GitHub-dark page on a
light OS would get the light version.

The stack lives in data/profile_config.yaml (`tech:`); logo paths and brand
colors come from data/tech_icons.json (vendored Simple Icons, CC0), so the
render needs no network. A brand color that would be too faint on a theme's
background is mixed toward white (dark) or black (light) until it reads.

Output: assets/tech-card-dark.svg, assets/tech-card-light.svg
"""

import json
import os

from make_info_card import esc, load_config

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS_PATH = os.path.join(ROOT, "data", "tech_icons.json")
OUT_PATTERN = os.path.join(ROOT, "assets", "tech-card-{theme}.svg")

FONT_FAMILY = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

MAX_WIDTH = 860       # wrap items past this; the SVG itself is cropped to fit
LABEL_FS = 13
NAME_FS = 14
CHAR_W = 0.6          # monospace advance, as a fraction of the font size
ROW_H = 30
ICON = 18
ICON_GAP = 8          # between an icon and its name
ITEM_GAP = 28         # between items on a row
GROUP_GAP = 10        # extra space between groups
LABEL_GAP = 24        # between the label column and the first item

THEMES = {
    "dark": {"bg": "#0d1117", "label": "#9198a1", "name": "#d1d7e0", "ok": "#3fb950",
             "min_contrast": 4.0, "toward": "#ffffff"},
    "light": {"bg": "#ffffff", "label": "#59636e", "name": "#1f2328", "ok": "#1a7f37",
              "min_contrast": 1.8, "toward": "#000000"},
}

# built-in glyph for tools without a Simple Icons logo (e.g. PHPUnit)
CHECK_PATH = "M4 12.5l5 5L20 6.5"


def _luminance(hex_color):
    rgb = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def _contrast(a, b):
    la, lb = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def _mix(hex_color, target, t):
    a = [int(hex_color[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(target[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def readable(hex_color, theme):
    """Nudge a brand color until it reaches the theme's minimum contrast."""
    t_cfg = THEMES[theme]
    color, t = hex_color, 0.0
    while _contrast(color, t_cfg["bg"]) < t_cfg["min_contrast"] and t < 1:
        t += 0.05
        color = _mix(hex_color, t_cfg["toward"], t)
    return color


def item_width(name):
    return ICON + ICON_GAP + len(name) * NAME_FS * CHAR_W


def layout(groups, items_x):
    """Place items per group, wrapping at MAX_WIDTH.

    Returns ([(label, y)], [(item, x, y)], width, height)."""
    labels, items = [], []
    y, right = 0.0, 0.0
    for group in groups:
        labels.append((group["group"], y))
        x = items_x
        for item in group["items"]:
            w = item_width(item["name"])
            if x > items_x and x + w > MAX_WIDTH:
                x = items_x
                y += ROW_H
            items.append((item, x, y))
            right = max(right, x + w)
            x += w + ITEM_GAP
        y += ROW_H + GROUP_GAP
    return labels, items, right, y - GROUP_GAP


def icon_svg(item, x, y, icons, theme):
    transform = f'translate({x:.1f},{y:.1f}) scale({ICON / 24:.4f})'
    if item["icon"] == "check":
        return (f'<path transform="{transform}" d="{CHECK_PATH}" fill="none" '
                f'stroke="{THEMES[theme]["ok"]}" stroke-width="3" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')
    icon = icons[item["icon"]]
    fill = readable("#" + icon["hex"], theme)
    return f'<path transform="{transform}" fill="{fill}" d="{icon["path"]}"/>'


def build_svg(groups, icons, theme):
    colors = THEMES[theme]
    label_w = max(len(g["group"]) for g in groups) * LABEL_FS * CHAR_W
    items_x = label_w + LABEL_GAP
    labels, items, width, height = layout(groups, items_x)
    width, height = round(width + 2), round(height)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT_FAMILY}">',
    ]
    for label, y in labels:
        baseline = y + ROW_H / 2 + LABEL_FS * 0.35
        svg.append(f'<text x="0" y="{baseline:.1f}" font-size="{LABEL_FS}" '
                   f'fill="{colors["label"]}">{esc(label)}</text>')
    for item, x, y in items:
        svg.append(icon_svg(item, x, y + (ROW_H - ICON) / 2, icons, theme))
        baseline = y + ROW_H / 2 + NAME_FS * 0.35
        svg.append(f'<text x="{x + ICON + ICON_GAP:.1f}" y="{baseline:.1f}" '
                   f'font-size="{NAME_FS}" fill="{colors["name"]}">{esc(item["name"])}</text>')
    svg.append("</svg>")
    return "\n".join(svg)


def main():
    groups = load_config().get("tech") or []
    with open(ICONS_PATH, "r", encoding="utf-8") as f:
        icons = json.load(f)["icons"]
    missing = {i["icon"] for g in groups for i in g["items"]} - set(icons) - {"check"}
    if missing:
        raise SystemExit(f"unknown icon(s) in profile_config.yaml: {', '.join(sorted(missing))}")
    for theme in THEMES:
        out_path = OUT_PATTERN.format(theme=theme)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(build_svg(groups, icons, theme))
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
