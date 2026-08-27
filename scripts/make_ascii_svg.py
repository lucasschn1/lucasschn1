#!/usr/bin/env python3
"""
make_ascii_svg.py

Content module for the whoami card: loads the ASCII portrait from
data/ascii_source.txt and returns it cropped + horizontally balanced. No SVG
is produced here anymore -- the single combined panel lives in
make_whoami_card.py.

Input: data/ascii_source.txt (raw ASCII art, one row per line)
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(ROOT, "data", "ascii_source.txt")


def load_rows():
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    # drop blank + detached-speck rows at the top/bottom so the figure itself
    # defines the bounding box (a stray fragment would otherwise pad the frame).
    SPECK = 12
    while lines and len(lines[0].strip()) < SPECK:
        lines.pop(0)
    while lines and len(lines[-1].strip()) < SPECK:
        lines.pop()

    ink = [ln for ln in lines if ln.strip()]
    if not ink:
        return lines

    # crop to the tight ink bounding box on the left, drop the right slack.
    left = min(len(ln) - len(ln.lstrip(" ")) for ln in ink)
    cropped = [ln[left:].rstrip() if ln.strip() else "" for ln in lines]

    # balance the figure: shift every row by the same amount so the ink
    # centroid lands on the middle of the frame (keeps pixel alignment while
    # correcting the diagonal lean).
    cols = [c for ln in cropped for c, ch in enumerate(ln) if ch != " "]
    widest = max((len(ln) for ln in cropped), default=0)
    if cols:
        centroid = sum(cols) / len(cols)
        shift = round(widest / 2 - centroid)
        if shift > 0:
            cropped = [" " * shift + ln if ln else "" for ln in cropped]
    return [ln.rstrip() if ln.strip() else "" for ln in cropped]
