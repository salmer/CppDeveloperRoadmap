#!/usr/bin/env python3
"""
extract — reverse the roadmap map into a mapgen DSL + translation file.

Parses <Lang>/Graph/roadmap.drawio.svg, reconstructs the skill tree by BFS over
structural edges from three anchor nodes (centre / left / right), and writes a
`structure.dsl` + `<lang>.tsv` that mapgen can regenerate.

  centre  "C++ developer" (id 12)   — the node both halves hang off
  left    "Soft skills"   (id 13)
  right   "Hard skills"   (id 14)  — parent of the hard-skills sections

Pink hint boxes (#FFD5E4) with curved arrows become `hint` directives; each node's
maturity `stage` is read from the #F5F5F5 "N step" frames by containment.

With --slugs (run on the EN map) the ids are word slugs and a words.tsv bridge is
written; other languages key their text onto those word-ids (--words, or remap.py).

Not yet extracted (see README): the legend swatches and title/About chrome blocks,
and a few isolated nodes whose parent link goes through non-skill connectors.

Usage:
  # canonical (word-ids + stages + words.tsv):
  python tools/mapgen/extract.py English/Graph/roadmap.drawio.svg -o tools/mapgen/roadmap --lang en --slugs
  # a language that shares EN's numeric ids (ZH): relabel onto the word-ids
  python tools/mapgen/extract.py Chinese/Graph/roadmap.drawio.svg -o tools/mapgen/roadmap --lang zh --words tools/mapgen/roadmap/words.tsv
"""
import argparse, html, math, os, re, sys
import xml.etree.ElementTree as ET
from collections import defaultdict, deque

GRADE = {"#96BB7C":"junior","#FAD586":"middle","#BBCCEE":"senior","#CCEEFF":"optional"}
HINT_FILL = "#FFD5E4"
STAGE_FILL = "#F5F5F5"

def slug(text):
    """A short word-id from English node text: lowercased, c++→cpp, parentheticals
    dropped, non-alphanumerics→'-', capped at 4 words. Ids are derived from the
    reference (EN) map only, so they stay language-neutral."""
    t = text.lower().replace("c++", "cpp").replace("&", "and").replace("/", " ")
    t = re.sub(r"\(.*?\)", "", t)
    t = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", t)).strip("-")
    parts = t.split("-")
    return "-".join(parts[:4]) if len(parts) > 4 else (t or "node")

def word_ids(verts, ids, parent):
    """Assign each numeric id a unique word slug; resolve collisions by qualifying
    with the parent's slug, then a numeric suffix. `ids` order decides who keeps the
    bare slug (shallower/earlier wins)."""
    base = {n: slug(verts[n]["text"]) for n in ids}
    final = {}
    for n in ids:
        s = base[n]
        if s in final.values():
            p = parent.get(n)
            s = f"{base.get(p,'')}-{base[n]}".strip("-") if p in base else base[n]
        o, i = s, 2
        while s in final.values():
            s = f"{o}-{i}"; i += 1
        final[n] = s
    return final

def stage_of(verts, parent):
    """Maturity stage per tree node, read from the #F5F5F5 'N step' frames by
    geometric containment (smallest containing frame wins). Language-neutral."""
    frames = [i for i in verts if verts[i]["fill"] == STAGE_FILL]
    step = {}
    for f in frames:
        m = re.search(r"(\d)", verts[f]["text"]); step[f] = int(m.group(1)) if m else 0
    def inside(n, f):
        a, b = verts[n], verts[f]; cx, cy = a["x"]+a["w"]/2, a["y"]+a["h"]/2
        return b["x"] <= cx <= b["x"]+b["w"] and b["y"] <= cy <= b["y"]+b["h"]
    stage = {}
    for n in parent:
        c = [f for f in frames if inside(n, f)]
        if c: stage[n] = step[min(c, key=lambda f: verts[f]["w"]*verts[f]["h"])]
    return stage

def stage_labels(verts):
    """{N: 'N step'} frame titles per language (EN '1 step', RU '1 этап', ZH '步骤 1').
    Emitted as stage1..stageN tsv keys; the generated stage frames title from them."""
    out = {}
    for v in verts.values():
        if v["fill"] != STAGE_FILL: continue
        m = re.search(r"(\d)", v["text"])
        if m: out.setdefault(int(m.group(1)), v["text"])
    return out

def chrome_cells(verts, tree):
    """The static top-left chrome: title, About/How-to/Feedback headers+bodies, repo
    link, date, and the legend swatches+descriptions — everything that is not a tree
    node, a hint, a stage frame, or the centre/anchors."""
    skip = tree | {"12", "13", "14"}
    return [v for i, v in verts.items()
            if i not in skip and v["fill"] not in (HINT_FILL, STAGE_FILL)]

def chrome_role(v):
    """Language-neutral role-id for a chrome block, from its EN text/shape."""
    if v["text"].lower().startswith("last updated"): return "last-updated"
    if v["link"]: return "repository-link"
    r = slug(v["text"])
    return ("legend-" + r) if v["fill"] in GRADE else r   # grade fill => legend swatch/desc

def match_chrome_by_id(en_layout, cells):
    """Match by draw.io id — for a language that shares the reference's chrome ids (ZH)."""
    by = {c["id"]: c for c in cells}
    return {e["role"]: by[e["id"]]["text"] for e in en_layout if e["id"] in by}

def match_chrome_by_position(en_layout, cells):
    """Match by nearest centroid — for a language whose chrome ids diverged but whose
    layout is preserved (RU)."""
    out, used = {}, set()
    for e in en_layout:
        ex, ey = e["x"]+e["w"]/2, e["y"]+e["h"]/2
        best, bd = None, 1e18
        for k, c in enumerate(cells):
            if k in used: continue
            d = (c["x"]+c["w"]/2-ex)**2 + (c["y"]+c["h"]/2-ey)**2
            if d < bd: bd, best = d, k
        if best is not None: out[e["role"]] = cells[best]["text"]; used.add(best)
    return out

def style_map(s):
    d = {}
    for p in (s or "").split(";"):
        if "=" in p:
            k, v = p.split("=", 1); d[k.strip()] = v.strip()
    return d

def load(svg_path):
    """Return (verts, edges). Handles UserObject/object wrappers (link-bearing
    nodes) whose id/label live on the wrapper and geometry on the inner mxCell."""
    svg = ET.parse(svg_path).getroot()
    model = ET.fromstring(svg.get("content"))
    verts, edges = {}, []
    def add_vertex(vid, label, cell, link=None):
        g = cell.find("mxGeometry")
        if g is None or g.get("width") is None:
            return
        st = style_map(cell.get("style"))
        txt = re.sub(r"\s+", " ",
            html.unescape(re.sub("<[^>]+>", "", label or "").replace("&#xa;", " "))).strip()
        verts[vid] = {"id":vid, "text":txt, "fill":st.get("fillColor",""),
            "x":float(g.get("x",0)), "y":float(g.get("y",0)),
            "w":float(g.get("width")), "h":float(g.get("height")),
            "style":cell.get("style") or "", "link":link}
    def add_edge(cell):
        st = style_map(cell.get("style"))
        edges.append({"s":cell.get("source"), "t":cell.get("target"), "curved":st.get("curved")=="1"})
    for el in model.iter():
        if el.tag in ("UserObject", "object"):
            cell = el.find("mxCell")
            if cell is None: continue
            if cell.get("vertex") == "1": add_vertex(el.get("id"), el.get("label"), cell, el.get("link"))
            elif cell.get("edge") == "1": add_edge(cell)
        elif el.tag == "mxCell":
            if el.get("vertex") == "1" and el.get("id"): add_vertex(el.get("id"), el.get("value"), el)
            elif el.get("edge") == "1": add_edge(el)
    return verts, edges

def build_tree(verts, edges, center="12", left="13", right="14"):
    """BFS a rooted tree from the left/right anchors over structural (non-curved)
    edges between graded nodes. Returns (parent, depth, kids). Shared with remap.py
    so both reconstruct the tree identically."""
    roots = [left, right]
    rootset = set(roots) | {center}
    content = {i for i, v in verts.items() if v["fill"] in GRADE}
    travers = content | rootset
    adj = defaultdict(set)
    for e in edges:
        if e["curved"]: continue
        if e["s"] in travers and e["t"] in travers:
            adj[e["s"]].add(e["t"]); adj[e["t"]].add(e["s"])
    parent, depth, kids = {}, {}, defaultdict(list)
    def grow(root):
        parent[root]=None; depth[root]=0; q=deque([root])
        while q:
            u=q.popleft()
            for v in sorted(adj[u], key=lambda n:(verts[n]["y"], verts[n]["x"])):
                if v in rootset and v != root: continue     # don't cross into another section
                if v in parent: continue
                parent[v]=u; depth[v]=depth[u]+1; kids[u].append(v); q.append(v)
    for r in roots: grow(r)
    return parent, depth, kids

def load_words(path):
    """Read words.tsv -> ordered list of (word, numeric_id)."""
    out = []
    for ln in open(path, encoding="utf-8"):
        if "\t" in ln and not ln.startswith("#"):
            w, n = ln.rstrip("\n").split("\t", 1); out.append((w, n))
    return out

def load_chrome(path):
    """Read chrome.tsv -> list of dict(role, id, x, y, w, h, link, style)."""
    out = []
    for ln in open(path, encoding="utf-8"):
        if ln.startswith("#") or "\t" not in ln: continue
        p = ln.rstrip("\n").split("\t")
        out.append({"role":p[0], "id":p[1], "x":float(p[2]), "y":float(p[3]), "w":float(p[4]),
                    "h":float(p[5]), "link":p[6] if len(p) > 6 else "",
                    "style":p[7] if len(p) > 7 else ""})
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("map", help="path to <Lang>/Graph/roadmap.drawio.svg")
    ap.add_argument("-o", "--out", required=True, help="output dir for structure.dsl + <lang>.tsv")
    ap.add_argument("--lang", default=None, help="tsv basename (default: from the map's parent dir)")
    ap.add_argument("--slugs", action="store_true",
                    help="reference mode: emit word-id structure.dsl + <lang>.tsv + words.tsv (run on the EN map)")
    ap.add_argument("--words", default=None,
                    help="relabel this map's tsv by the word-ids in the given words.tsv (for a language that shares the reference's numeric ids, e.g. ZH)")
    ap.add_argument("--chrome", default=None,
                    help="with --words: also emit chrome text, matched to the roles in this chrome.tsv by position")
    ap.add_argument("--center", default="12")
    ap.add_argument("--left", default="13")
    ap.add_argument("--right", default="14")
    args = ap.parse_args()

    verts, edges = load(args.map)
    CENTER, LEFT, RIGHT = args.center, args.left, [args.right]
    lang = args.lang or os.path.normpath(args.map).split(os.sep)[-3][:2].lower()
    parent, depth, kids = build_tree(verts, edges, CENTER, LEFT, RIGHT[0])
    os.makedirs(args.out, exist_ok=True)

    # --words: relabel a shared-id language's text onto the reference word-ids
    if args.words:
        rows = [f"{w}\t{verts[n]['text']}" for w, n in load_words(args.words) if n in verts]
        rows += [f"stage{n}\t{lab}" for n, lab in sorted(stage_labels(verts).items())]
        if args.chrome:   # ZH shares the reference chrome ids -> match by id
            ct = match_chrome_by_id(load_chrome(args.chrome), chrome_cells(verts, set(parent)))
            rows += [f"{role}\t{text}" for role, text in ct.items()]
        open(os.path.join(args.out, f"{lang}.tsv"), "w", encoding="utf-8").write("\n".join(rows)+"\n")
        print(f"relabeled {len(rows)} entries onto word-ids -> {args.out}/{lang}.tsv")
        return

    # pre-order node list (also the tsv/dsl order) and hint list
    order = []
    def walk(nid):
        order.append(nid)
        for c in sorted(kids[nid], key=lambda n:(verts[n]['y'], verts[n]['x'])): walk(c)
    for r in sorted([LEFT]+RIGHT, key=lambda r: verts[r]["y"]): walk(r)
    hint_ids = []
    order_set = set(order)
    for hid, v in sorted(verts.items(), key=lambda kv:(kv[1]["y"], kv[1]["x"])):
        if v["fill"] != HINT_FILL: continue      # a pink box's arrows may be curved OR straight
        if [t for t in (e["t"] for e in edges if e["s"]==hid) if t in order_set]:
            hint_ids.append(hid)

    # id -> emitted key: numeric, or word slug in --slugs mode
    key = {n: n for n in [CENTER]+order+hint_ids}
    if args.slugs:
        key = word_ids(verts, [CENTER]+order+hint_ids, parent)
    stage = stage_of(verts, parent)

    dsl = ["# Auto-extracted from " + os.path.basename(args.map) + " by tools/mapgen/extract.py.",
           "# centre / left / right anchors; pink boxes -> hints. See extract.py header.",
           "", f"spine center={key[CENTER]}", ""]
    tsv = [f"{key[CENTER]}\t{verts[CENTER]['text']}"]
    def emit(nid, d, side):
        toks = f" side={side}" if d == 0 else ""
        toks += f" grade={GRADE.get(verts[nid]['fill'],'junior')}"
        if stage.get(nid) != stage.get(parent.get(nid)):   # stage root: emit inherited value
            toks += f" stage={stage[nid]}"
        dsl.append("  "*d + f"[{key[nid]}]{toks}")
        tsv.append(f"{key[nid]}\t{verts[nid]['text']}")
        for c in sorted(kids[nid], key=lambda n:(verts[n]['y'], verts[n]['x'])):
            emit(c, d+1, side)
    for r, side in sorted([(LEFT,"left")] + [(r,"right") for r in RIGHT],
                          key=lambda rs: verts[rs[0]]["y"]):
        emit(r, 0, side); dsl.append("")

    for hid in hint_ids:
        tids = [t for t in (e["t"] for e in edges if e["s"]==hid) if t in key]
        targets = [key[t] for t in tids]
        # polar offset (angle deg, dist px) from the mean target centre to the box centre.
        # Captures the hand map's exact note placement so build.ps1 replays it verbatim
        # (draw.io is the output) instead of re-deriving it — auto-placement can't match a
        # hand-tuned layout. 0deg = right, 90deg = up. build.ps1 auto-places if omitted.
        hcx = verts[hid]["x"] + verts[hid]["w"]/2
        hcy = verts[hid]["y"] + verts[hid]["h"]/2
        tcx = sum(verts[t]["x"]+verts[t]["w"]/2 for t in tids)/len(tids)
        tcy = sum(verts[t]["y"]+verts[t]["h"]/2 for t in tids)/len(tids)
        ang = round(math.degrees(math.atan2(-(hcy-tcy), hcx-tcx))) % 360
        dist = round(math.hypot(hcx-tcx, hcy-tcy))
        dsl.append(f"hint [{key[hid]}] angle={ang} dist={dist} -> " + ", ".join(targets))
        tsv.append(f"{key[hid]}\t{verts[hid]['text']}")
    for n, lab in sorted(stage_labels(verts).items()):     # stage frame titles (translatable)
        tsv.append(f"stage{n}\t{lab}")

    # chrome: extracted only in reference (--slugs) mode; defines the static layer's
    # layout (chrome.tsv) and the reference text (into <lang>.tsv). Roles are assigned
    # from EN; other languages match their chrome to these roles by position.
    chrome_layout = []
    if args.slugs:
        seen = set()
        for v in sorted(chrome_cells(verts, set(parent)), key=lambda v:(v["y"], v["x"])):
            role, i = chrome_role(v), 2
            base = role
            while role in seen: role = f"{base}-{i}"; i += 1
            seen.add(role); chrome_layout.append((role, v))
            tsv.append(f"{role}\t{v['text']}")

    open(os.path.join(args.out, "structure.dsl"), "w", encoding="utf-8").write("\n".join(dsl)+"\n")
    open(os.path.join(args.out, f"{lang}.tsv"), "w", encoding="utf-8").write("\n".join(tsv)+"\n")
    staged = sum(1 for n in order if stage.get(n) != stage.get(parent.get(n)))
    print(f"extracted {len(order)} nodes, {len(hint_ids)} hints, {staged} stage roots"
          + (" (word-ids)" if args.slugs else " (numeric ids)"))
    if args.slugs:
        wrows = [f"{key[n]}\t{n}" for n in [CENTER]+order+hint_ids]
        open(os.path.join(args.out, "words.tsv"), "w", encoding="utf-8").write("\n".join(wrows)+"\n")
        crows = ["# role\tid\tx\ty\tw\th\tlink\tstyle"]
        crows += [f"{role}\t{v['id']}\t{v['x']:.0f}\t{v['y']:.0f}\t{v['w']:.0f}\t{v['h']:.0f}\t{v['link'] or ''}\t{v['style']}"
                  for role, v in chrome_layout]
        open(os.path.join(args.out, "chrome.tsv"), "w", encoding="utf-8").write("\n".join(crows)+"\n")
        print(f"wrote {args.out}/structure.dsl, {lang}.tsv, words.tsv, chrome.tsv ({len(chrome_layout)} chrome cells)")
    else:
        print(f"wrote {args.out}/structure.dsl and {lang}.tsv")

if __name__ == "__main__":
    sys.exit(main())
