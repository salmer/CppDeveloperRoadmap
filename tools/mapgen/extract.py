#!/usr/bin/env python3
"""
extract — reverse the roadmap map into a mapgen DSL + translation file.

Parses <Lang>/Graph/roadmap.drawio.svg, reconstructs the skill tree by BFS over
structural edges from three anchor nodes (centre / left / right), and writes a
`structure.dsl` + `<lang>.tsv` that mapgen can regenerate.

  centre  "C++ developer" (id 12)   — the node both halves hang off
  left    "Soft skills"   (id 13)
  right   "Hard skills"   (id 14)  — parent of the hard-skills sections

Pink hint boxes (#FFD5E4) with curved arrows become `hint` directives.

Notes / not yet extracted (decorative — see README): stage frames (#F5F5F5),
the legend swatches and the title/About blocks, and a few isolated nodes whose
parent link goes through non-skill connectors. Node text is language-specific;
run once per map to get each `<lang>.tsv`.

Usage:
  python tools/mapgen/extract.py English/Graph/roadmap.drawio.svg -o tools/mapgen/examples/fullmap
"""
import argparse, html, os, re, sys
import xml.etree.ElementTree as ET
from collections import defaultdict, deque

GRADE = {"#96BB7C":"junior","#FAD586":"middle","#BBCCEE":"senior","#CCEEFF":"optional"}
HINT_FILL = "#FFD5E4"

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
    def add_vertex(vid, label, cell):
        g = cell.find("mxGeometry")
        if g is None or g.get("width") is None:
            return
        st = style_map(cell.get("style"))
        txt = html.unescape(re.sub("<[^>]+>", "", label or "").replace("&#xa;", " ")).strip()
        verts[vid] = {"id":vid, "text":txt, "fill":st.get("fillColor",""),
            "x":float(g.get("x",0)), "y":float(g.get("y",0)),
            "w":float(g.get("width")), "h":float(g.get("height"))}
    def add_edge(cell):
        st = style_map(cell.get("style"))
        edges.append({"s":cell.get("source"), "t":cell.get("target"), "curved":st.get("curved")=="1"})
    for el in model.iter():
        if el.tag in ("UserObject", "object"):
            cell = el.find("mxCell")
            if cell is None: continue
            if cell.get("vertex") == "1": add_vertex(el.get("id"), el.get("label"), cell)
            elif cell.get("edge") == "1": add_edge(cell)
        elif el.tag == "mxCell":
            if el.get("vertex") == "1" and el.get("id"): add_vertex(el.get("id"), el.get("value"), el)
            elif el.get("edge") == "1": add_edge(el)
    return verts, edges

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("map", help="path to <Lang>/Graph/roadmap.drawio.svg")
    ap.add_argument("-o", "--out", required=True, help="output dir for structure.dsl + <lang>.tsv")
    ap.add_argument("--lang", default=None, help="tsv basename (default: from the map's parent dir)")
    ap.add_argument("--center", default="12")
    ap.add_argument("--left", default="13")
    ap.add_argument("--right", default="14")
    args = ap.parse_args()

    verts, edges = load(args.map)
    CENTER, LEFT, RIGHT = args.center, args.left, [args.right]
    roots = [LEFT] + RIGHT
    rootset = set(roots) | {CENTER}
    lang = args.lang or os.path.normpath(args.map).split(os.sep)[-3][:2].lower()

    content = {i for i,v in verts.items() if v["fill"] in GRADE}
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

    used = set()
    dsl = ["# Auto-extracted from " + os.path.basename(args.map) + " by tools/mapgen/extract.py.",
           "# centre / left / right anchors; pink boxes -> hints. See extract.py header.",
           "", f"spine center={CENTER}", ""]
    tsv = [f"{CENTER}\t{verts[CENTER]['text']}"]
    def emit(nid, d, side):
        used.add(nid)
        s = f" side={side}" if d == 0 else ""
        dsl.append("  "*d + f"[{nid}]{s} grade={GRADE.get(verts[nid]['fill'],'junior')}")
        tsv.append(f"{nid}\t{verts[nid]['text']}")
        for c in sorted(kids[nid], key=lambda n:(verts[n]['y'], verts[n]['x'])):
            emit(c, d+1, side)
    for r, side in sorted([(LEFT,"left")] + [(r,"right") for r in RIGHT],
                          key=lambda rs: verts[rs[0]]["y"]):
        emit(r, 0, side); dsl.append("")

    # hints: pink boxes whose curved arrows point at extracted nodes
    hints = 0
    for hid, v in verts.items():
        if v["fill"] != HINT_FILL: continue
        targets = [e["t"] for e in edges if e["s"]==hid and e["curved"] and e["t"] in used]
        if not targets: continue
        dsl.append(f"hint [{hid}] -> " + ", ".join(targets))
        tsv.append(f"{hid}\t{v['text']}")
        hints += 1

    os.makedirs(args.out, exist_ok=True)
    open(os.path.join(args.out, "structure.dsl"), "w", encoding="utf-8").write("\n".join(dsl)+"\n")
    open(os.path.join(args.out, f"{lang}.tsv"), "w", encoding="utf-8").write("\n".join(tsv)+"\n")
    total_skill = sum(1 for v in verts.values() if v["fill"] in GRADE)
    print(f"extracted {len(used)} nodes ({total_skill-len(used)} skill nodes unreached), {hints} hints")
    print(f"wrote {args.out}/structure.dsl and {lang}.tsv")

if __name__ == "__main__":
    sys.exit(main())
