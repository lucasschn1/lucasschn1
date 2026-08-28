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
  - build_lines() from make_info_card    (neofetch-style info lines)

Output: assets/whoami-card.svg
"""

import html
import os
import re

from make_ascii_svg import load_rows
from make_info_card import (
    CONTRIB_PATH,
    STATS_PATH,
    build_lines,
    esc,
    load_config,
    load_json,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(ROOT, "assets", "whoami-card.svg")

FONT_FAMILY = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

# ---- info panel -----------------------------------------------------
INFO_FS = 16.5
INFO_CHAR_W = INFO_FS * 0.6
INFO_LINE_H = INFO_FS * 1.6

# ---- portrait (font auto-fit so its height tracks the info block) ----
ART_LINE_RATIO = 1.18
ART_FS_MIN, ART_FS_MAX = 9.0, 16.0

PAD = 36
GAP = 44

# ---- theme (dark defaults, light override via @media) ---------------
THEME_CSS = """
  :root{
    --bg:#0d1117; --border:#30363d;
    --name:#c9d1d9; --label:#e8b98c; --value:#c9d1d9; --dim:#5a626c;
    --add:#3fb950; --del:#f85149;
  }
  @media (prefers-color-scheme: light){
    :root{
      --bg:#ffffff; --border:#d0d7de;
      --name:#1f2328; --label:#a15c1e; --value:#1f2328; --dim:#9aa4af;
      --add:#1a7f37; --del:#cf222e;
    }
  }
  .panel{fill:var(--bg);stroke:var(--border);}
  .art{fill:var(--value);}
  .row{fill:var(--value);}
  .head{fill:var(--name);}
  .label{fill:var(--label);}
  .dim{fill:var(--dim);}
  .add{fill:var(--add);}
  .del{fill:var(--del);}
"""


def fit_art_fs(rows, target_h):
    """Pick the portrait font size so its rendered height ~= target_h."""
    n = max(len(rows), 1)
    fs = target_h / (n * ART_LINE_RATIO)
    return max(ART_FS_MIN, min(ART_FS_MAX, fs))


def measure_art(rows, fs):
    w = max((len(r) for r in rows), default=0) * fs * 0.6
    h = len(rows) * fs * ART_LINE_RATIO
    return w, h


def measure_info(lines):
    max_chars = max((len(t) for k, t in lines if t), default=40)
    h = 0.0
    for kind, _ in lines:
        h += INFO_LINE_H * (0.5 if kind == "blank" else 1.0)
    return max_chars * INFO_CHAR_W, h, max_chars


def art_svg(rows, x0, y0, fs):
    line_h = fs * ART_LINE_RATIO
    out = [f'<g font-size="{fs:.2f}" class="art">']
    for i, line in enumerate(rows):
        if not line.strip():
            continue
        y = y0 + i * line_h + fs
        out.append(
            f'<text x="{x0:.1f}" y="{y:.1f}" xml:space="preserve">'
            f'{html.escape(line)}</text>'
        )
    out.append("</g>")
    return out


# token -> tspan class, tried in order; anything unmatched renders as plain value
_ROW_TOKENS = [
    (re.compile(r"\.{2,}"), "dim"),                 # dot leaders
    (re.compile(r"[\d,]+\+\+"), "add"),             # "111,399++"
    (re.compile(r"[\d,]+--"), "del"),               # "52,018--"
    (re.compile(r"[A-Za-z][\w.()/ ]*?: "), "label"),  # "Languages.Programming: "
]


def _row_spans(text):
    text = esc(text)
    # leading ". " prefix -> faint
    prefix = ""
    if text.startswith(". "):
        prefix, text = '<tspan class="dim">. </tspan>', text[2:]
    out, i = [prefix], 0
    while i < len(text):
        for rx, cls in _ROW_TOKENS:
            m = rx.match(text, i)
            if m:
                out.append(f'<tspan class="{cls}">{m.group(0)}</tspan>')
                i = m.end()
                break
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def _head_spans(text):
    text = esc(text)
    m = re.search(r"-{2,}.*$", text)
    if not m:
        return text
    return f'{text[:m.start()]}<tspan class="dim">{text[m.start():]}</tspan>'


def info_svg(lines, x0, y0):
    out = [f'<g font-size="{INFO_FS}" xml:space="preserve">']
    y = y0 + INFO_FS
    for kind, text in lines:
        if kind == "blank":
            y += INFO_LINE_H * 0.5
            continue
        if kind in ("top", "section"):
            out.append(f'<text class="head" x="{x0:.1f}" y="{y:.2f}">{_head_spans(text)}</text>')
        else:
            out.append(f'<text class="row" x="{x0:.1f}" y="{y:.2f}">{_row_spans(text)}</text>')
        y += INFO_LINE_H
    out.append("</g>")
    return out


def build_svg(rows, lines):
    info_w, info_h, max_chars = measure_info(lines)
    art_fs = fit_art_fs(rows, info_h)
    art_w, art_h = measure_art(rows, art_fs)

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
    svg += art_svg(rows, art_x, art_y, art_fs)
    svg += info_svg(lines, info_x, info_y)
    svg.append("</svg>")
    return "\n".join(svg)


def main():
    rows = load_rows()
    lines = build_lines(load_config(), load_json(STATS_PATH), load_json(CONTRIB_PATH))
    svg = build_svg(rows, lines)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(rows)} art rows, {len(lines)} info lines)")


if __name__ == "__main__":
    main()
