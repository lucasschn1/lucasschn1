#!/usr/bin/env python3
"""
make_info_card.py

Content module for the whoami card: turns data/profile_config.yaml into the
neofetch-style key/value rows that make_whoami_card.py renders. No SVG is
produced here -- the single combined panel lives in make_whoami_card.py.
"""

import html
import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, "data", "profile_config.yaml")

LABEL_COL = 24  # character column where the dot leaders end


def kv(label, value, col=LABEL_COL):
    prefix = f"{label}: "
    dots = " " if len(prefix) >= col else "." * (col - len(prefix))
    return f"{prefix}{dots} {value}"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_lines(cfg):
    """Returns a list of (kind, text) tuples.

    kind: 'header' | 'rule' | 'kv' | 'blank'
    """
    lines = []
    lines.append(("header", f"{cfg['username']}@github"))
    lines.append(("rule", None))

    lines.append(("kv", kv("OS", cfg["os"])))
    lines.append(("kv", kv("Role", cfg["role"])))
    lines.append(("kv", kv("IDE", cfg["ide"])))
    lines.append(("blank", None))

    lines.append(("kv", kv("Languages.Code", ", ".join(cfg["languages_programming"]))))
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

    return lines


def esc(s):
    return html.escape(s, quote=False)
