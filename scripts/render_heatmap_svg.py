#!/usr/bin/env python3
"""
render_heatmap_svg.py

Reads data/contributions.json (written by fetch_contributions.py) and draws
the classic 53-week x 7-day contribution calendar as rounded, colored boxes
using a GitHub-ish green ramp. The grid reveals once, diagonally, with each
box sliding into place (CSS keyframes with animation-delay, `forwards` so it
freezes at the end -- no looping). Adds a Less->More legend and a stats
footer.

Colors are driven by CSS custom properties with a
`@media (prefers-color-scheme: light)` override, so the single SVG adapts to
GitHub's light and dark themes on its own.

Output: assets/contrib-heatmap.svg
"""

import datetime
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "contributions.json")
OUT_PATH = os.path.join(ROOT, "assets", "contrib-heatmap.svg")

# CSS class per contribution level (0..4); "rec" is the single record-day
# highlight. Actual colors live in THEME_CSS (dark default + light override).
CELL_CLASS = ["l0", "l1", "l2", "l3", "l4", "rec"]

STAGGER = 0.012
CELL_ANIM_DUR = 0.35

THEME_CSS = """
  :root{
    --text:#7d8590; --footer:#c9d1d9;
    --l0:#161b22; --l1:#0e4429; --l2:#006d32;
    --l3:#26a641; --l4:#39d353; --rec:#69f0a0;
  }
  @media (prefers-color-scheme: light){
    :root{
      --text:#57606a; --footer:#1f2328;
      --l0:#ebedf0; --l1:#9be9a8; --l2:#40c463;
      --l3:#30a14e; --l4:#216e39; --rec:#1a7f37;
    }
  }
  text{font-size:10px;fill:var(--text);}
  .footer{font-size:12px;fill:var(--footer);}
  .l0{fill:var(--l0);} .l1{fill:var(--l1);} .l2{fill:var(--l2);}
  .l3{fill:var(--l3);} .l4{fill:var(--l4);} .rec{fill:var(--rec);}
  .cell{opacity:0;transform:translateY(-6px);
        animation:slideIn %.2fs ease-out forwards;}
  @keyframes slideIn{
    from{opacity:0;transform:translateY(-6px);}
    to{opacity:1;transform:translateY(0);}
  }
""" % CELL_ANIM_DUR

WEEKS = 53
DAYS = 7
CELL = 11
GAP = 3
RADIUS = 2
LEFT_PAD = 28   # room for weekday labels
TOP_PAD = 20    # room for month labels
RIGHT_PAD = 12
BOTTOM_PAD = 46  # room for legend + footer stats

FONT_FAMILY = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WEEKDAY_LABELS = {1: "Mon", 3: "Wed", 5: "Fri"}  # dow index -> label


def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def build_grid(data):
    by_date = {d["date"]: d for d in data.get("days", []) if d.get("date")}

    if by_date:
        end_date = max(datetime.date.fromisoformat(d) for d in by_date)
    else:
        end_date = datetime.date.today()

    total_days = WEEKS * DAYS
    end_dow = (end_date.weekday() + 1) % 7  # convert Mon=0..Sun=6 -> Sun=0..Sat=6
    # the grid's last column must end on end_date; walk back to that column's Sunday
    last_col_sunday = end_date - datetime.timedelta(days=end_dow)
    start_date = last_col_sunday - datetime.timedelta(days=(WEEKS - 1) * 7)

    grid = []  # list of {week, dow, date, level, count}
    best = None
    for i in range(total_days):
        d = start_date + datetime.timedelta(days=i)
        if d > end_date:
            level, count = 0, 0
            present = False
        else:
            entry = by_date.get(d.isoformat())
            if entry:
                level = entry.get("level", 0)
                count = entry.get("count")
            else:
                level, count = 0, None
            present = True
        cell = {
            "week": i // 7,
            "dow": i % 7,
            "date": d.isoformat(),
            "level": level,
            "count": count,
            "present": present,
        }
        grid.append(cell)
        if present and count is not None:
            if best is None or count > best["count"]:
                best = cell

    return grid, start_date, end_date, best


def month_label_positions(grid):
    """Return {week_index: label} for the first week where a new month starts."""
    labels = {}
    seen_months = set()
    for cell in grid:
        if cell["dow"] != 0:
            continue
        d = datetime.date.fromisoformat(cell["date"])
        key = (d.year, d.month)
        if key not in seen_months:
            seen_months.add(key)
            labels[cell["week"]] = MONTH_ABBR[d.month - 1]
    return labels


def main():
    data = load_data()
    grid, start_date, end_date, best = build_grid(data)
    month_labels = month_label_positions(grid)

    grid_w = WEEKS * (CELL + GAP) - GAP
    grid_h = DAYS * (CELL + GAP) - GAP
    width = LEFT_PAD + grid_w + RIGHT_PAD
    height = TOP_PAD + grid_h + BOTTOM_PAD

    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT_FAMILY}">'
    )
    svg.append(f'<rect width="100%" height="100%" fill="transparent"/>')
    svg.append(f'<style>{THEME_CSS}</style>')

    # month labels
    for week_idx, label in month_labels.items():
        x = LEFT_PAD + week_idx * (CELL + GAP)
        svg.append(f'<text x="{x}" y="{TOP_PAD - 7}">{label}</text>')

    # weekday labels
    for dow, label in WEEKDAY_LABELS.items():
        y = TOP_PAD + dow * (CELL + GAP) + CELL - 2
        svg.append(f'<text x="0" y="{y}">{label}</text>')

    # cells, diagonal stagger: delay grows with (week + dow)
    for cell in grid:
        x = LEFT_PAD + cell["week"] * (CELL + GAP)
        y = TOP_PAD + cell["dow"] * (CELL + GAP)
        level = min(cell["level"], 4)
        cls = CELL_CLASS[level]
        if best is not None and cell["date"] == best["date"]:
            cls = CELL_CLASS[5]
        delay = (cell["week"] + cell["dow"]) * STAGGER
        title = f'{cell["date"]}: {cell["count"] if cell["count"] is not None else "?"} contributions'
        svg.append(
            f'<rect class="cell {cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
            f'rx="{RADIUS}" ry="{RADIUS}" style="animation-delay:{delay:.3f}s">'
            f'<title>{title}</title></rect>'
        )

    # legend: Less [boxes] More
    legend_y = TOP_PAD + grid_h + 18
    legend_x = LEFT_PAD
    svg.append(f'<text x="{legend_x}" y="{legend_y + CELL - 2}">Less</text>')
    lx = legend_x + 34
    for cls in CELL_CLASS[:5]:
        svg.append(
            f'<rect class="{cls}" x="{lx}" y="{legend_y}" width="{CELL}" height="{CELL}" '
            f'rx="{RADIUS}" ry="{RADIUS}"/>'
        )
        lx += CELL + GAP
    svg.append(f'<text x="{lx + 6}" y="{legend_y + CELL - 2}">More</text>')

    # footer stats
    total = data.get("total_contributions")
    streak = data.get("current_streak")
    footer_y = legend_y + 24
    footer_parts = []
    if total is not None:
        footer_parts.append(f"{total} contributions in the last year")
    if streak:
        footer_parts.append(f"current streak: {streak} days")
    if footer_parts:
        svg.append(f'<text class="footer" x="{LEFT_PAD}" y="{footer_y}">{" | ".join(footer_parts)}</text>')

    svg.append("</svg>")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"wrote {OUT_PATH}: {start_date} -> {end_date}, total={total}")


if __name__ == "__main__":
    main()
