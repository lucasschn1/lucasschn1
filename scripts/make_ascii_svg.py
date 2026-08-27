#!/usr/bin/env python3
"""
make_ascii_svg.py

Turns a block of ASCII art text into a self-typing, monochrome animated SVG.
Each row wipes in left-to-right (SMIL <animate> on a clip-path), staggered
top to bottom, with a small block "cursor" riding the wipe edge. The whole
thing plays once and freezes -- no looping.

Input:  data/ascii_source.txt   (raw ASCII art, one row per line)
Output: assets/ascii-portrait.svg
"""

import html
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(ROOT, "data", "ascii_source.txt")
OUT_PATH = os.path.join(ROOT, "assets", "ascii-portrait.svg")

# ---- look & feel -----------------------------------------------------
FONT_FAMILY = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"
FONT_SIZE = 15.5
CHAR_W = FONT_SIZE * 0.6      # monospace advance width (em-relative)
LINE_H = FONT_SIZE * 1.05
PAD_X = 10
PAD_Y = 10
FILL_COLOR = "#c9d1d9"        # single, monochrome, light-gray-ish (dark-theme friendly)
BG_COLOR = "transparent"

# ---- animation timing --------------------------------------------------
ROW_DURATION = 0.55           # seconds each row takes to wipe in
STAGGER = 0.045               # seconds between the start of consecutive rows
CURSOR_W = CHAR_W * 0.85
CURSOR_H = LINE_H * 0.82


def load_rows():
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        raw = f.read()
    # keep trailing spaces meaningful, but drop a fully-blank leading/trailing
    # line that's just an artifact of how the block was pasted/saved.
    lines = raw.split("\n")
    while lines and lines[0].strip() == "":
        lines.pop(0)
    while lines and lines[-1].strip() == "":
        lines.pop()
    # strip the common leading whitespace so the art sits tight in the
    # viewBox (keeps it visually centered when embedded at a fixed width).
    # base the dedent on the "body" rows (ignore short detached specks so a
    # stray fragment doesn't pin the whole block to the left edge).
    body = [ln for ln in lines if len(ln.strip()) >= 20]
    ref = body or [ln for ln in lines if ln.strip()]
    if ref:
        indent = min(len(ln) - len(ln.lstrip(" ")) for ln in ref)
        if indent:
            lines = [ln[min(indent, len(ln) - len(ln.lstrip(" "))):]
                     if ln.strip() else ln for ln in lines]
    return [ln.rstrip() for ln in lines]


def build_svg(rows):
    n_rows = len(rows)
    max_len = max((len(r) for r in rows), default=0)

    width = PAD_X * 2 + max_len * CHAR_W
    height = PAD_Y * 2 + n_rows * LINE_H

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width:.1f}" height="{height:.1f}" '
        f'viewBox="0 0 {width:.1f} {height:.1f}" font-family="{FONT_FAMILY}">'
    )
    parts.append(f'<rect width="100%" height="100%" fill="{BG_COLOR}"/>')
    parts.append(
        f'<style>text{{font-size:{FONT_SIZE}px;fill:{FILL_COLOR};}}'
        f'.cursor{{fill:{FILL_COLOR};}}</style>'
    )

    defs = ["<defs>"]
    body = []

    for i, raw_line in enumerate(rows):
        row_width = len(raw_line) * CHAR_W
        row_y = PAD_Y + i * LINE_H
        baseline = row_y + LINE_H * 0.85
        begin = i * STAGGER
        clip_id = f"row-clip-{i}"
        escaped = html.escape(raw_line).replace(" ", " ") if raw_line.strip() == "" else html.escape(raw_line)

        defs.append(
            f'<clipPath id="{clip_id}">'
            f'<rect x="0" y="{row_y:.2f}" width="0" height="{LINE_H:.2f}">'
            f'<animate attributeName="width" from="0" to="{row_width + PAD_X:.2f}" '
            f'begin="{begin:.3f}s" dur="{ROW_DURATION:.2f}s" '
            f'calcMode="spline" keySplines="0.2 0 0.2 1" fill="freeze"/>'
            f'</rect></clipPath>'
        )

        if raw_line.strip():
            body.append(
                f'<g clip-path="url(#{clip_id})">'
                f'<text x="{PAD_X}" y="{baseline:.2f}" xml:space="preserve">{escaped}</text>'
                f'</g>'
            )

            # block cursor riding the wipe edge, then vanishing once the row is done
            body.append(
                f'<rect class="cursor" y="{row_y + LINE_H * 0.12:.2f}" '
                f'width="{CURSOR_W:.2f}" height="{CURSOR_H:.2f}" x="{PAD_X}">'
                f'<animate attributeName="x" from="{PAD_X}" to="{PAD_X + row_width:.2f}" '
                f'begin="{begin:.3f}s" dur="{ROW_DURATION:.2f}s" '
                f'calcMode="spline" keySplines="0.2 0 0.2 1" fill="freeze"/>'
                f'<animate attributeName="opacity" values="1;1;0" keyTimes="0;0.9;1" '
                f'begin="{begin:.3f}s" dur="{ROW_DURATION:.2f}s" fill="freeze"/>'
                f'</rect>'
            )

    defs.append("</defs>")

    parts.extend(defs)
    parts.extend(body)
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    rows = load_rows()
    svg = build_svg(rows)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
