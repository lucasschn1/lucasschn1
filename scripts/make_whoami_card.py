#!/usr/bin/env python3
"""
make_whoami_card.py

Renders ONE static terminal-style panel with the ASCII portrait and the
neofetch-style info side by side -- no animation. This replaces the previously
separate assets/ascii-portrait.svg + assets/info-card.svg pair.

Colors are driven by CSS custom properties with a
`@media (prefers-color-scheme: light)` override, so the single SVG adapts to
GitHub's light and dark themes on its own (no <picture> needed).

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
ART_FS = 10.5
ART_CHAR_W = ART_FS * 0.6
ART_LINE_H = ART_FS * 1.18

# ---- info panel -----------------------------------------------------
INFO_FS = 18.0
INFO_CHAR_W = INFO_FS * 0.6
INFO_LINE_H = INFO_FS * 1.8

PAD = 36
GAP = 40

# ---- theme (dark defaults, light override via @media) ---------------
THEME_CSS = """
  :root{
    --bg:#0d1117; --border:#30363d;
    --header:#39d353; --value:#c9d1d9; --rule:#30363d;
  }
  @media (prefers-color-scheme: light){
    :root{
      --bg:#ffffff; --border:#d0d7de;
      --header:#1a7f37; --value:#1f2328; --rule:#d0d7de;
    }
  }
  .panel{fill:var(--bg);stroke:var(--border);}
  .art,.value{fill:var(--value);}
  .header{fill:var(--header);font-weight:600;}
  .rule{stroke:var(--rule);}
"""


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
    out = [f'<g font-size="{ART_FS}" class="art">']
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
                f'<line class="rule" x1="{x0:.1f}" y1="{yy:.2f}" '
                f'x2="{x0 + max_chars * INFO_CHAR_W:.1f}" y2="{yy:.2f}"/>'
            )
            y += INFO_LINE_H * 0.6
            continue
        if kind == "blank":
            y += INFO_LINE_H * 0.55
            continue
        cls = "header" if kind == "header" else "value"
        out.append(
            f'<text class="{cls}" x="{x0:.1f}" y="{y:.2f}" '
            f'xml:space="preserve">{esc(text)}</text>'
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
        f'<style>{THEME_CSS}</style>',
        f'<rect class="panel" x="0.5" y="0.5" width="{width - 1:.1f}" '
        f'height="{height - 1:.1f}" rx="10"/>',
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
