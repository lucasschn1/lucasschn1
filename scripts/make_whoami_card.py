#!/usr/bin/env python3
"""
make_whoami_card.py

Renders ONE static terminal-style panel with the ASCII portrait and the
neofetch-style info side by side -- no animation. This replaces the previously
separate assets/ascii-portrait.svg + assets/info-card.svg pair.

Row/line content is reused from the existing renderers:
  - load_rows()   from make_ascii_svg   (cropped + centered ASCII art)
  - build_lines() from make_info_card    (OS/Role/IDE/... key-value rows)

Output: assets/whoami-card.svg
"""

import html
import os

from make_ascii_svg import load_rows
from make_info_card import build_lines, esc, load_config

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "assets", "whoami-card.svg")

FONT_FAMILY = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

# ---- portrait --------------------------------------------------------
ART_FS = 11.0
ART_CHAR_W = ART_FS * 0.6
ART_LINE_H = ART_FS * 1.05
ART_FILL = "#c9d1d9"

# ---- info panel -----------------------------------------------------
INFO_FS = 13.0
INFO_CHAR_W = INFO_FS * 0.6
INFO_LINE_H = INFO_FS * 1.55

PAD = 26
GAP = 40

PANEL_BG = "#0d1117"
PANEL_BORDER = "#30363d"
COLOR_HEADER = "#39d353"
COLOR_VALUE = "#c9d1d9"
COLOR_RULE = "#30363d"


def measure_art(rows):
    w = max((len(r) for r in rows), default=0) * ART_CHAR_W
    h = len(rows) * ART_LINE_H
    return w, h


def measure_info(lines):
    max_chars = max((len(t) for k, t in lines if t), default=40)
    h = 0.0
    for kind, _ in lines:
        if kind == "rule":
            h += INFO_LINE_H * 0.6
        elif kind == "blank":
            h += INFO_LINE_H * 0.55
        else:
            h += INFO_LINE_H
    return max_chars * INFO_CHAR_W, h, max_chars


def art_svg(rows, x0, y0):
    out = [f'<g font-size="{ART_FS}" fill="{ART_FILL}">']
    for i, line in enumerate(rows):
        if not line.strip():
            continue
        y = y0 + i * ART_LINE_H + ART_FS
        out.append(
            f'<text x="{x0:.1f}" y="{y:.1f}" xml:space="preserve">'
            f'{html.escape(line)}</text>'
        )
    out.append("</g>")
    return out


def info_svg(lines, x0, y0, max_chars):
    out = [f'<g font-size="{INFO_FS}">']
    y = y0 + INFO_FS
    for kind, text in lines:
        if kind == "rule":
            yy = y - INFO_FS * 0.4
            out.append(
                f'<line x1="{x0:.1f}" y1="{yy:.2f}" '
                f'x2="{x0 + max_chars * INFO_CHAR_W:.1f}" y2="{yy:.2f}" '
                f'stroke="{COLOR_RULE}"/>'
            )
            y += INFO_LINE_H * 0.6
            continue
        if kind == "blank":
            y += INFO_LINE_H * 0.55
            continue
        color = COLOR_HEADER if kind == "header" else COLOR_VALUE
        weight = " font-weight='600'" if kind == "header" else ""
        out.append(
            f'<text x="{x0:.1f}" y="{y:.2f}" xml:space="preserve" '
            f'fill="{color}"{weight}>{esc(text)}</text>'
        )
        y += INFO_LINE_H
    out.append("</g>")
    return out


def build_svg(rows, lines):
    art_w, art_h = measure_art(rows)
    info_w, info_h, max_chars = measure_info(lines)

    content_h = max(art_h, info_h)
    width = PAD * 2 + art_w + GAP + info_w
    height = PAD * 2 + content_h

    art_x = PAD
    art_y = PAD + (content_h - art_h) / 2
    info_x = PAD + art_w + GAP
    info_y = PAD + (content_h - info_h) / 2

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.1f}" '
        f'height="{height:.1f}" viewBox="0 0 {width:.1f} {height:.1f}" '
        f'font-family="{FONT_FAMILY}">',
        f'<rect x="0.5" y="0.5" width="{width - 1:.1f}" height="{height - 1:.1f}" '
        f'rx="10" fill="{PANEL_BG}" stroke="{PANEL_BORDER}"/>',
    ]
    svg += art_svg(rows, art_x, art_y)
    svg += info_svg(lines, info_x, info_y, max_chars)
    svg.append("</svg>")
    return "\n".join(svg)


def main():
    rows = load_rows()
    lines = build_lines(load_config())
    svg = build_svg(rows, lines)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(rows)} art rows, {len(lines)} info lines)")


if __name__ == "__main__":
    main()
