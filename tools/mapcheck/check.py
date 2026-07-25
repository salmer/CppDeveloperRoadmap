#!/usr/bin/env python3
"""
mapcheck — validate the roadmap maps (<Lang>/Graph/roadmap.drawio.svg).

Checks (per the conventions in AGENTS.md):
  A1  box-fits-text : a node whose label is wider than its box (the "C++26 box
                      too narrow" class of bug).            [hard error]
      overlaps      : two content nodes whose boxes overlap.  [hard error]
      date          : "Last updated" older than the map file's last commit.  [warning]
  A2  drift         : the maps' vertical structure must match across languages
                      (shared y-rows, per AGENTS.md); a row present in one
                      language but not another is drift.      [warning]

Pure-XML/geometry checks need only Python's stdlib. box-fits-text also needs
Pillow + a font; without them it is skipped with a note (so CI still runs the
geometry checks). Exit code is non-zero if any hard error is found.

Usage:
  python tools/mapcheck/check.py                # all maps under <Lang>/Graph
  python tools/mapcheck/check.py --maps English/Graph/roadmap.drawio.svg
  python tools/mapcheck/check.py --no-date      # skip the git-based date check
"""
import argparse, html, re, subprocess, sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

try:
    from PIL import ImageFont
except Exception:
    ImageFont = None

FRAME_FILL = "#F5F5F5"          # stage frames (containers) — overlap everything by design
DEFAULT_FONT_SIZE = 20
OVERLAP_TOL = 1.0               # ignore <=1px touches
# box-fits-text: flag only when the label is over the box by BOTH an absolute and
# a relative margin. Liberation Sans == Arial (exact for Latin); CJK metrics
# (Noto) only approximate draw.io's, so the relative margin absorbs that noise
# while still catching gross overflows like the old 72px-box "C++26 (newest)".
OVERFLOW_ABS = 6.0
OVERFLOW_REL = 0.10

LATIN_FONTS = [                 # Liberation Sans == Arial metrics (what draw.io uses)
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/Library/Fonts/Arial.ttf",
]
CJK_FONTS = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "C:/Windows/Fonts/msyh.ttc",
]


def first_existing(paths):
    for p in paths:
        if Path(p).exists():
            return p
    return None


def style_map(style):
    out = {}
    for part in (style or "").split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def load_cells(svg_path):
    """Return (vertices, n_edges) from the embedded draw.io XML in a .drawio.svg.
    Each vertex is {id,text,fill,wrap,x,y,w,h,size}."""
    svg = ET.parse(svg_path).getroot()
    content = svg.get("content")
    if not content:
        raise SystemExit(f"{svg_path}: no embedded draw.io content")
    model = ET.fromstring(content)          # attribute is already un-escaped by ET
    verts, n_edges = [], 0
    for cell in model.iter("mxCell"):
        if cell.get("edge") == "1":
            n_edges += 1
            continue
        if cell.get("vertex") != "1":
            continue
        geo = cell.find("mxGeometry")
        if geo is None or geo.get("width") is None:
            continue
        st = style_map(cell.get("style"))
        raw = cell.get("value") or ""
        text = re.sub(r"<[^>]+>", "", raw).replace("&#xa;", "\n")
        text = html.unescape(text)
        verts.append({
            "id": cell.get("id"),
            "text": text,
            "fill": st.get("fillColor", ""),
            "wrap": st.get("whiteSpace") == "wrap",
            "size": float(st.get("fontSize", DEFAULT_FONT_SIZE)),
            "x": float(geo.get("x", 0)), "y": float(geo.get("y", 0)),
            "w": float(geo.get("width")), "h": float(geo.get("height")),
        })
    return verts, n_edges


# ---------- fonts / measurement ----------
_cache = {}

def get_font(path, size):
    key = (path, int(size))
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, int(size))
    return _cache[key]

def _is_cjk(c):
    o = ord(c)
    return 0x3000 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF or 0xFF00 <= o <= 0xFFEF

def measure(text, size, latin, cjk):
    # sum per-character so mixed Latin+CJK lines aren't over-measured by forcing
    # the whole run through the (wider) CJK font
    total = 0.0
    for c in text:
        path = cjk if (_is_cjk(c) and cjk) else latin
        total += get_font(path, size).getlength(c)
    return total


# ---------- checks ----------
def check_box_fits(name, verts, latin, cjk):
    """Returns (hard, warn). Latin labels are measured with Arial-exact metrics
    -> hard error. CJK labels use approximate metrics -> warning only."""
    hard, warn = [], []
    for v in verts:
        if v["wrap"] or v["fill"] == FRAME_FILL or not v["text"].strip():
            continue
        widest = max((measure(line, v["size"], latin, cjk)
                      for line in v["text"].splitlines() if line), default=0)
        if widest > v["w"] + OVERFLOW_ABS and widest > v["w"] * (1 + OVERFLOW_REL):
            msg = (f'  [{name}] node {v["id"]} "{v["text"][:40]}": '
                   f'text ~{widest:.0f}px > box {v["w"]:.0f}px')
            if any(_is_cjk(c) for c in v["text"]):
                warn.append(msg + "  (CJK, approx metrics)")
            else:
                hard.append(msg)
    return hard, warn


def check_overlaps(name, verts):
    items = [v for v in verts if v["fill"] != FRAME_FILL]
    errs = []
    for i in range(len(items)):
        a = items[i]
        for j in range(i + 1, len(items)):
            b = items[j]
            ox = min(a["x"]+a["w"], b["x"]+b["w"]) - max(a["x"], b["x"])
            oy = min(a["y"]+a["h"], b["y"]+b["h"]) - max(a["y"], b["y"])
            if ox > OVERLAP_TOL and oy > OVERLAP_TOL:
                errs.append(f'  [{name}] nodes {a["id"]} "{a["text"][:24]}" & '
                            f'{b["id"]} "{b["text"][:24]}" overlap '
                            f'{ox:.0f}x{oy:.0f}px')
    return errs


def check_date(name, svg_path, verts):
    cell = (next((v for v in verts if v["id"] == "n1100"), None)
            or next((v for v in verts if v["text"].strip().lower().startswith("last updated")), None))
    if not cell:
        return [f"  [{name}] no 'Last updated' box (id n1100) found"]
    m = re.search(r"(\d{4})[-.](\d{2})[-.](\d{2})|(\d{2})\.(\d{2})\.(\d{4})", cell["text"])
    if not m:
        return [f"  [{name}] can't parse date from '{cell['text']}'"]
    if m.group(1):
        emb = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    else:
        emb = f"{m.group(6)}-{m.group(5)}-{m.group(4)}"
    try:
        commit = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs", "--", str(svg_path)],
            text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return []
    if commit and emb < commit:
        return [f"  [{name}] 'Last updated: {emb}' is older than last commit ({commit}) — bump it"]
    return []


def check_drift(stats):
    """stats: {name: {'vertices':n,'edges':n,'colors':Counter}}. The maps must
    match in node/edge counts; a mismatch means a change landed in one language
    but not the others. (Coarse by design: exact per-node y positions differ
    slightly across languages, so counts are the robust drift signal.)"""
    names = list(stats)
    if len(names) < 2:
        return []
    errs = []
    for key in ("vertices", "edges"):
        vals = {n: stats[n][key] for n in names}
        if len(set(vals.values())) > 1:
            errs.append(f"  {key}: " + ", ".join(f"{n}={vals[n]}" for n in names))
    all_c = set().union(*[set(stats[n]["colors"]) for n in names])
    for c in sorted(all_c):
        vals = {n: stats[n]["colors"].get(c, 0) for n in names}
        if len(set(vals.values())) > 1:
            errs.append(f"  fill {c or '(none)'}: " + ", ".join(f"{n}={vals[n]}" for n in names))
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maps", nargs="*", help="explicit .drawio.svg paths (default: autodiscover)")
    ap.add_argument("--no-date", action="store_true")
    ap.add_argument("--strict", action="store_true", help="also fail on drift/warnings")
    ap.add_argument("--latin-font", default=None)
    ap.add_argument("--cjk-font", default=None)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    root = Path(__file__).resolve().parents[2]
    if args.maps:
        maps = [(Path(p).stem.split(".")[0], Path(p)) for p in args.maps]
        maps = [(Path(p).parts[-3] if len(Path(p).parts) >= 3 else n, Path(p)) for n, p in maps]
    else:
        maps = [(p.parts[-3], p) for p in sorted(root.glob("*/Graph/roadmap.drawio.svg"))]
    if not maps:
        print("no maps found"); return 1

    latin = args.latin_font or first_existing(LATIN_FONTS)
    cjk = args.cjk_font or first_existing(CJK_FONTS)
    can_measure = ImageFont is not None and latin is not None

    hard, warn = [], []
    stats = {}
    for name, path in maps:
        verts, n_edges = load_cells(path)
        stats[name] = {"vertices": len(verts), "edges": n_edges,
                       "colors": Counter(v["fill"] for v in verts)}
        if can_measure:
            h, w = check_box_fits(name, verts, latin, cjk)
            hard += h; warn += w
        hard += check_overlaps(name, verts)
        if not args.no_date:
            warn += check_date(name, path, verts)
        print(f"scanned {name}: {len(verts)} vertices, {n_edges} edges")

    drift = check_drift(stats)

    def section(title, items):
        print(f"\n=== {title} ({len(items)}) ===")
        for it in items:
            print(it)

    if not can_measure:
        print("\n[note] Pillow/font unavailable — box-fits-text check skipped")
    section("HARD ERRORS (box-fits-text, overlaps)", hard)
    section("cross-language drift (rows differing across maps)", drift)
    section("warnings (date)", warn)

    print()
    if hard:
        print(f"FAIL: {len(hard)} hard error(s)")
        return 1
    if args.strict and (drift or warn):
        print(f"FAIL (--strict): {len(drift)} drift + {len(warn)} warning(s)")
        return 1
    print("OK: no hard errors" + (f"; {len(drift)} drift + {len(warn)} warning(s)" if drift or warn else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
