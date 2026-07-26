#!/usr/bin/env python3
"""
build — generate a draw.io map from a language-neutral DSL + per-language translations.

Reads <dir>/structure.dsl (topology, grades, stages, hints, frames, spine) and
<dir>/<lang>.tsv (id <TAB> text), computes the physical layout per language (widths from
text metrics, local packing, bus routing, polar hint placement), emits mxGraph XML, renders
it through the draw.io desktop CLI, and restores the light-dark background. The built
<lang>.drawio.svg is then copied over the live <Lang>/Graph/roadmap.drawio.svg.

The DSL fixes the *logical* layout (rows, order, grade, stage, hint offsets, spine sides);
this computes the *physical* layout (x, width, waypoints, frame size) so the same structure
reflows for each language's text width. Text metrics use Pillow (the same library mapcheck
measures with), so the generator and the checker agree on widths.

Usage:
  python tools/mapgen/build.py --dir tools/mapgen/roadmap
  python tools/mapgen/build.py --dir tools/mapgen/roadmap --langs en,zh
"""
import argparse, math, os, subprocess, sys, time
from PIL import ImageFont

# ---- layout constants (match the map's conventions; see README) ----
H, PITCH, GAP, MARGIN, FONTSIZE, PADX = 30, 60, 40, 40, 20, 12
HINT_W, HINT_GAP, LINEH, PADV, SPINE_STUB, STAGE_GAP = 320, 90, 24, 9, 90, 90
FPAD, FTITLE = 24, 50
GRADES = {"junior": "#96BB7C", "middle": "#FAD586", "senior": "#BBCCEE", "optional": "#CCEEFF"}
HINT_FILL, FRAME_FILL = "#FFD5E4", "#F5F5F5"
# YaHei covers Latin + Cyrillic + CJK (what the PowerShell build measured via System.Drawing)
FONT_CANDIDATES = ["C:/Windows/Fonts/msyh.ttc", "C:/Windows/Fonts/msyh.ttf",
                   "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]


def num(v):
    """Format a coordinate: integers without a decimal, else trimmed to 3 places."""
    v = float(v)
    return str(int(v)) if v == int(v) else ("%.3f" % v).rstrip("0").rstrip(".")


def xml_esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


# ---- text measurement (Pillow; same approach as tools/mapcheck) ----
def make_measure(font_path):
    font = ImageFont.truetype(font_path, FONTSIZE)

    def measure(t):
        return float(font.getlength(t))
    return measure


def is_cjk(ch):
    o = ord(ch)
    return 0x3000 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF or 0xFF00 <= o <= 0xFFEF


def wrap(text, maxw, measure):
    """Wrap to maxw. Tokenize so CJK (no spaces) wraps too: Latin words stay whole,
    spaces are explicit tokens, each CJK char is its own token."""
    tokens, buf = [], ""
    for ch in text:
        if ch == " ":
            if buf:
                tokens.append(buf); buf = ""
            tokens.append(" ")
        elif is_cjk(ch):
            if buf:
                tokens.append(buf); buf = ""
            tokens.append(ch)
        else:
            buf += ch
    if buf:
        tokens.append(buf)
    lines, cur = [], ""
    for tk in tokens:
        trial = cur + " " if tk == " " else cur + tk
        if measure(trial) <= maxw or cur == "":
            cur = trial
        else:
            lines.append(cur.rstrip())
            cur = "" if tk == " " else tk
    if cur.strip():
        lines.append(cur.rstrip())
    return lines or [text]


# ---- parse DSL: nodes (by indent) + hint / frame / spine directives ----
def parse_dsl(path):
    nodes, order, stack, hints, frames, spine = {}, [], {}, [], [], None
    import re
    for ln in open(path, encoding="utf-8").read().splitlines():
        t = ln.strip()
        if t == "" or t.startswith("#"):
            continue
        if re.match(r"^spine\b", t):
            spine = {"hubx": None, "gate": None, "header": None, "center": None}
            m = re.search(r"hubx=(\d+)", t);   spine["hubx"] = float(m.group(1)) if m else None
            m = re.search(r"gate=(\d+)", t);   spine["gate"] = float(m.group(1)) if m else None
            m = re.search(r"header=(\S+)", t); spine["header"] = m.group(1) if m else None
            m = re.search(r"center=(\S+)", t); spine["center"] = m.group(1) if m else None
            continue
        m = re.match(r"^frame\s+\[([^\]]+)\]", t)
        if m:
            fid = m.group(1)
            mt = re.search(r"title=(\S+)", t)
            mc = re.search(r"contains=(\S+)", t)
            frames.append({"id": fid, "titleKey": mt.group(1) if mt else None,
                           "contains": [x.strip() for x in mc.group(1).split(",")] if mc else None})
            continue
        m = re.match(r"^hint\s+\[([^\]]+)\]\s*(.*?)->\s*(.+)$", t)
        if m:
            hid, attr, tg = m.group(1), m.group(2), [x.strip() for x in m.group(3).split(",")]
            ma = re.search(r"angle=(-?\d+(?:\.\d+)?)", attr)
            md = re.search(r"dist=(\d+(?:\.\d+)?)", attr)
            mr = re.search(r"arrow=(left|right|top|bottom)", attr)
            hints.append({"id": hid, "targets": tg,
                          "angle": float(ma.group(1)) if ma else None,
                          "dist": float(md.group(1)) if md else None,
                          "arrow": mr.group(1) if mr else None})
            continue
        indent = len(ln) - len(ln.lstrip())
        depth = indent // 2
        m = re.search(r"\[([^\]]+)\]", ln)
        if not m:
            continue
        nid = m.group(1)
        mg = re.search(r"grade=(\w+)", ln); grade = mg.group(1) if mg else "junior"
        parent = stack.get(depth - 1) if depth > 0 else None
        ms = re.search(r"side=(left|right)", ln)
        side = ms.group(1) if ms else (nodes[parent]["side"] if parent else "right")
        mst = re.search(r"stage=(\d+)", ln)
        stage = int(mst.group(1)) if mst else (nodes[parent]["stage"] if parent else None)
        nodes[nid] = {"id": nid, "grade": grade, "depth": depth, "parent": parent,
                      "side": side, "stage": stage, "children": []}
        if parent:
            nodes[parent]["children"].append(nid)
        stack[depth] = nid
        order.append(nid)
    return nodes, order, hints, frames, spine


def load_chrome(path):
    chrome = []
    if not os.path.exists(path):
        return chrome
    for l in open(path, encoding="utf-8").read().splitlines():
        if l.strip() == "" or l.startswith("#"):
            continue
        p = l.split("\t")   # role, id, x, y, w, h, link, style
        chrome.append({"role": p[0], "x": float(p[2]), "y": float(p[3]),
                       "w": float(p[4]), "h": float(p[5]),
                       "link": p[6] if len(p) > 6 else "", "style": p[7] if len(p) > 7 else ""})
    return chrome


def descendants(nodes, rid):
    acc = [rid]
    for c in nodes[rid]["children"]:
        acc += descendants(nodes, c)
    return acc


def section_of(nodes, nid):
    n = nodes[nid]
    while n["parent"] and nodes[n["parent"]]["depth"] >= 1:
        n = nodes[n["parent"]]
    return n["id"]


def build_lang(lang, dsl, chrome, args, measure, drawio_dir):
    nodes, order, hints, frames, spine = dsl
    tr_path = os.path.join(args.dir, f"{lang}.tsv")
    if not os.path.exists(tr_path):
        print(f"  {lang} SKIPPED (no {lang}.tsv)"); return
    tr = {}
    for l in open(tr_path, encoding="utf-8").read().splitlines():
        if l.strip() == "":
            continue
        p = l.split("\t", 1)
        tr[p[0]] = p[1] if len(p) > 1 else ""

    # node text + width (physical width from this language's text)
    for nid in order:
        txt = tr.get(nid, nid)
        nodes[nid]["text"] = txt
        nodes[nid]["width"] = math.ceil(measure(txt) + 2 * PADX)

    # ---- vertical layout: leaves at row pitch (+ stage gaps), parent = midpoint of kids
    state = {"row": 0, "off": 0.0, "prev": None}

    def assign_y(nid):
        n = nodes[nid]
        if not n["children"]:
            k = f"{section_of(nodes, nid)}#{n['stage']}" if n["stage"] is not None else None
            if k is not None and state["prev"] is not None and k != state["prev"]:
                state["off"] += STAGE_GAP
            n["cy"] = MARGIN + state["row"] * PITCH + state["off"] + H / 2
            state["row"] += 1
            if k is not None:
                state["prev"] = k
        else:
            for c in n["children"]:
                assign_y(c)
            n["cy"] = (nodes[n["children"][0]]["cy"] + nodes[n["children"][-1]]["cy"]) / 2

    for want in ("right", "left"):   # each half stacks from the top -> two parallel columns
        state.update(row=0, off=0.0, prev=None)
        for nid in order:
            n = nodes[nid]
            if n["depth"] == 0 and (n["side"] == "left") == (want == "left"):
                assign_y(nid)

    # centre node: shift both halves so their midpoints line up on it
    center_w, center_y = 0, None
    if spine and spine["center"]:
        ctext = tr.get(spine["center"], spine["center"])
        center_w = math.ceil(measure(ctext) + 2 * PADX)
        rt = lt = 1e18; rb = lb = -1e18
        for nid in order:
            n = nodes[nid]
            if n["side"] == "left":
                lt = min(lt, n["cy"] - H / 2); lb = max(lb, n["cy"] + H / 2)
            else:
                rt = min(rt, n["cy"] - H / 2); rb = max(rb, n["cy"] + H / 2)
        rH, lH = max(0, rb - rt), max(0, lb - lt)
        center_y = MARGIN + max(rH, lH) / 2
        if rb > rt:
            dy = center_y - (rt + rb) / 2
            for nid in order:
                if nodes[nid]["side"] != "left":
                    nodes[nid]["cy"] += dy
        if lb > lt:
            dy = center_y - (lt + lb) / 2
            for nid in order:
                if nodes[nid]["side"] == "left":
                    nodes[nid]["cy"] += dy

    # push the whole tree below the full-width title banner
    if chrome:
        title_bottom = max((c["y"] + c["h"] for c in chrome if c["w"] > 2000), default=0.0)
        tree_top = min(nodes[nid]["cy"] - H / 2 for nid in order)
        need = (title_bottom + MARGIN) - tree_top
        if need > 0:
            for nid in order:
                nodes[nid]["cy"] += need
            if center_y is not None:
                center_y += need

    # pin section roots to the centre row (horizontal C++ developer | Soft | Hard line)
    if spine and spine["center"] and center_y is not None:
        for nid in order:
            if nodes[nid]["depth"] == 0:
                nodes[nid]["cy"] = center_y

    # ---- horizontal layout: LOCAL packing (child just right/left of its own parent)
    def layout_x(nid, x, direction):
        nodes[nid]["x"] = x
        n = nodes[nid]
        for c in n["children"]:
            cx = n["x"] + n["width"] + 2 * GAP if direction == 1 else n["x"] - 2 * GAP - nodes[c]["width"]
            layout_x(c, cx, direction)

    eff_stub = center_w / 2 + 2 * GAP if center_w > 0 else SPINE_STUB
    left_roots = [nid for nid in order if nodes[nid]["depth"] == 0 and nodes[nid]["side"] == "left"]
    right_roots = [nid for nid in order if nodes[nid]["depth"] == 0 and nodes[nid]["side"] != "left"]
    hubx = 0.0
    if spine:
        hubx = spine["hubx"] if spine["hubx"] else 460.0
        if left_roots:
            for nid in left_roots:
                layout_x(nid, -eff_stub - nodes[nid]["width"], -1)   # relative to hub=0
            leftmost = min(nodes[nid]["x"] for nid in order if nodes[nid]["side"] == "left")
            if not spine["hubx"]:
                hubx = MARGIN - leftmost
        if chrome and not spine["hubx"]:                              # clear the top-left chrome column
            chrome_right = max(c["x"] + c["w"] for c in chrome)
            hubx = max(hubx, chrome_right + GAP - eff_stub)
        if left_roots:
            for nid in order:
                if nodes[nid]["side"] == "left":
                    nodes[nid]["x"] += hubx
        for nid in right_roots:
            layout_x(nid, hubx + eff_stub, 1)
    else:
        for nid in right_roots:
            layout_x(nid, MARGIN, 1)

    # ---- hints: size box, place at polar offset (angle deg, dist px) from mean target centre
    for hn in hints:
        txt = tr.get(hn["id"], hn["id"])
        wl = wrap(txt, HINT_W - 2 * PADX, measure)
        hn["lines"] = wl
        hn["width"] = HINT_W
        hn["height"] = max(H, len(wl) * LINEH + 2 * PADV)
        cxs = [nodes[t]["x"] + nodes[t]["width"] / 2 for t in hn["targets"] if t in nodes]
        cys = [nodes[t]["cy"] for t in hn["targets"] if t in nodes]
        tcx = sum(cxs) / len(cxs) if cxs else 0.0
        tcy = sum(cys) / len(cys) if cys else 0.0
        ang = hn["angle"] if hn["angle"] is not None else 0.0
        dst = hn["dist"] if hn["dist"] is not None else HINT_GAP + hn["width"] / 2
        rad = math.radians(ang)
        hcx = tcx + dst * math.cos(rad)
        hcy = tcy - dst * math.sin(rad)
        hn["x"] = hcx - hn["width"] / 2
        hn["cy"] = hcy
        hn["tcx"], hn["tcy"] = tcx, tcy

    # ---- emit mxGraph XML ----
    sb = ['<mxfile host="mapgen"><diagram name="frag" id="frag"><mxGraphModel dx="0" dy="0" '
          'grid="0" pageWidth="850" pageHeight="1100" background="#ffffff" math="0" shadow="0"><root>',
          '<mxCell id="0"/><mxCell id="1" parent="0"/>']
    frame_style = (f"rounded=0;html=0;fillColor={FRAME_FILL};strokeColor=#000000;strokeWidth=1;"
                   f"fontSize=28;fontColor=#000000;fontFamily={args.font_family};verticalAlign=top;"
                   "align=center;fontStyle=1;container=0;")

    def frame_cell(cid, members, title):
        minX = min(nodes[i]["x"] for i in members)
        maxX = max(nodes[i]["x"] + nodes[i]["width"] for i in members)
        minY = min(nodes[i]["cy"] - H / 2 for i in members)
        maxY = max(nodes[i]["cy"] + H / 2 for i in members)
        fx, fy = minX - FPAD, minY - FTITLE
        fw, fh = (maxX - minX) + 2 * FPAD, (maxY - minY) + FTITLE + FPAD
        return (f'<mxCell id="{cid}" parent="1" vertex="1" style="{frame_style}" value="{xml_esc(title)}">'
                f'<mxGeometry x="{num(fx)}" y="{num(fy)}" width="{num(fw)}" height="{num(fh)}" as="geometry"/></mxCell>')

    # explicit frames (behind everything)
    for fr in frames:
        members = [x for r in fr["contains"] for x in descendants(nodes, r)] if fr["contains"] else order
        title = tr.get(fr["titleKey"], "") if fr["titleKey"] else ""
        sb.append(frame_cell(fr["id"], members, title))
    # auto stage frames grouped by (section, stage)
    groups = {}
    for nid in order:
        if nodes[nid]["stage"] is None:
            continue
        groups.setdefault(f"{section_of(nodes, nid)}#{nodes[nid]['stage']}", []).append(nid)
    for i, (k, members) in enumerate(groups.items()):
        stage_num = k.split("#")[1]
        sb.append(frame_cell(f"_stage_{i}", members, tr.get(f"stage{stage_num}", stage_num)))

    # spine: trunk + optional gate/header + root stubs + centre node
    if spine:
        gate = spine["gate"]
        root_ids = [nid for nid in order if nodes[nid]["depth"] == 0]
        rc = [nodes[i]["cy"] for i in root_ids]
        minR, maxR = min(rc), max(rc)
        hcy = (minR + maxR) / 2
        top = min(nodes[i]["cy"] - H / 2 for i in order)
        bot = max(nodes[i]["cy"] + H / 2 for i in order)
        y0, y1 = min(minR, hcy), max(maxR, hcy)
        if gate and gate > 0:
            sb.append(f'<mxCell id="_gate" parent="1" edge="1" style="endArrow=none;html=0;strokeColor=#999999;dashed=1;">'
                      f'<mxGeometry relative="1" as="geometry"><mxPoint x="{num(gate)}" y="{num(top-20)}" as="sourcePoint"/>'
                      f'<mxPoint x="{num(gate)}" y="{num(bot+20)}" as="targetPoint"/></mxGeometry></mxCell>')
            sb.append(f'<mxCell id="_gatelbl" parent="1" vertex="1" style="text;html=0;fontSize=14;fontColor=#999999;align=center;" '
                      f'value="gate"><mxGeometry x="{num(gate-20)}" y="{num(top-44)}" width="40" height="18" as="geometry"/></mxCell>')
        sb.append(f'<mxCell id="_trunk" parent="1" edge="1" style="endArrow=none;html=0;strokeColor=#000000;strokeWidth=1;">'
                  f'<mxGeometry relative="1" as="geometry"><mxPoint x="{num(hubx)}" y="{num(y0)}" as="sourcePoint"/>'
                  f'<mxPoint x="{num(hubx)}" y="{num(y1)}" as="targetPoint"/></mxGeometry></mxCell>')
        if spine["header"]:
            htext = tr.get(spine["header"], spine["header"])
            hw = math.ceil(measure(htext) + 2 * PADX); hx = gate - hw - 24; hy = hcy - H / 2
            st = (f"rounded=0;html=0;fillColor=#96BB7C;strokeColor=#000000;strokeWidth=1;fontSize={FONTSIZE};"
                  f"fontColor=#000000;fontFamily={args.font_family};verticalAlign=middle;align=center;")
            sb.append(f'<mxCell id="_hdr" parent="1" vertex="1" style="{st}" value="{xml_esc(htext)}">'
                      f'<mxGeometry x="{num(hx)}" y="{num(hy)}" width="{num(hw)}" height="{H}" as="geometry"/></mxCell>')
            sb.append(f'<mxCell id="_hdrstub" parent="1" edge="1" source="_hdr" style="edgeStyle=none;html=0;endArrow=none;'
                      f'strokeColor=#000000;exitX=1;exitY=0.5;exitDx=0;exitDy=0;"><mxGeometry relative="1" as="geometry">'
                      f'<mxPoint x="{num(hubx)}" y="{num(hcy)}" as="targetPoint"/></mxGeometry></mxCell>')
        for nid in root_ids:
            entry = 1 if nodes[nid]["side"] == "left" else 0
            sb.append(f'<mxCell id="_s_{nid}" parent="1" edge="1" target="{nid}" style="edgeStyle=none;html=0;endArrow=none;'
                      f'strokeColor=#000000;entryX={entry};entryY=0.5;entryDx=0;entryDy=0;"><mxGeometry relative="1" as="geometry">'
                      f'<mxPoint x="{num(hubx)}" y="{num(nodes[nid]["cy"])}" as="sourcePoint"/></mxGeometry></mxCell>')
        if spine["center"]:
            ct = tr.get(spine["center"], spine["center"])
            st = (f"rounded=1;html=0;fillColor=#FFE5B9;strokeColor=#000000;strokeWidth=1;fontSize={FONTSIZE};"
                  f"fontColor=#000000;fontFamily={args.font_family};verticalAlign=middle;align=center;fontStyle=1;")
            sb.append(f'<mxCell id="_center" parent="1" vertex="1" style="{st}" value="{xml_esc(ct)}">'
                      f'<mxGeometry x="{num(hubx-center_w/2)}" y="{num(center_y-H/2)}" width="{num(center_w)}" height="{H}" as="geometry"/></mxCell>')

    # nodes
    for nid in order:
        n = nodes[nid]
        st = (f"rounded=0;html=0;fillColor={GRADES[n['grade']]};strokeColor=#000000;strokeWidth=1;fontSize={FONTSIZE};"
              f"fontColor=#000000;fontFamily={args.font_family};verticalAlign=middle;align=center;")
        sb.append(f'<mxCell id="{nid}" parent="1" vertex="1" style="{st}" value="{xml_esc(n["text"])}">'
                  f'<mxGeometry x="{num(n["x"])}" y="{num(n["cy"]-H/2)}" width="{num(n["width"])}" height="{H}" as="geometry"/></mxCell>')

    # hint boxes (line breaks already inserted by wrap; no whiteSpace=wrap)
    for hn in hints:
        val = "&#xa;".join(xml_esc(l) for l in hn["lines"])
        st = (f"rounded=0;html=0;fillColor={HINT_FILL};strokeColor=#000000;strokeWidth=1;fontSize={FONTSIZE};"
              f"fontColor=#000000;fontFamily={args.font_family};verticalAlign=middle;align=center;")
        sb.append(f'<mxCell id="{hn["id"]}" parent="1" vertex="1" style="{st}" value="{val}">'
                  f'<mxGeometry x="{num(hn["x"])}" y="{num(hn["cy"]-hn["height"]/2)}" '
                  f'width="{num(hn["width"])}" height="{num(hn["height"])}" as="geometry"/></mxCell>')

    # chrome: static top-left blocks at absolute coords, text per language
    for c in chrome:
        txt = tr.get(c["role"], c["role"])
        st = c["style"]
        if "whiteSpace=" not in st:
            st = f"{st};whiteSpace=wrap;"
        g = (f'<mxGeometry x="{num(c["x"])}" y="{num(c["y"])}" width="{num(c["w"])}" height="{num(c["h"])}" as="geometry"/>')
        if c["link"]:
            sb.append(f'<UserObject id="{c["role"]}" label="{xml_esc(txt)}" link="{xml_esc(c["link"])}">'
                      f'<mxCell parent="1" vertex="1" style="{st}">{g}</mxCell></UserObject>')
        else:
            sb.append(f'<mxCell id="{c["role"]}" parent="1" vertex="1" style="{st}" value="{xml_esc(txt)}">{g}</mxCell>')

    # parent -> child edges (orthogonal via the column bus)
    for nid in order:
        n = nodes[nid]
        if not n["children"]:
            continue
        if n["side"] == "left":
            busx, ex, en = n["x"] - GAP, 0, 1
        else:
            busx, ex, en = n["x"] + n["width"] + GAP, 1, 0
        for cid in n["children"]:
            c = nodes[cid]
            st = (f"edgeStyle=none;html=0;strokeColor=#000000;strokeWidth=1;startArrow=none;endArrow=none;rounded=0;"
                  f"exitX={ex};exitY=0.5;exitDx=0;exitDy=0;entryX={en};entryY=0.5;entryDx=0;entryDy=0;")
            sb.append(f'<mxCell id="e_{cid}" parent="1" edge="1" source="{nid}" target="{cid}" style="{st}">'
                      f'<mxGeometry relative="1" as="geometry"><Array as="points">'
                      f'<mxPoint x="{num(busx)}" y="{num(n["cy"])}"/><mxPoint x="{num(busx)}" y="{num(c["cy"])}"/>'
                      f'</Array></mxGeometry></mxCell>')

    # hint arrows: from a box edge (start side) to each target's facing edge
    for hn in hints:
        bcx, bcy = hn["x"] + hn["width"] / 2, hn["cy"]
        if hn["arrow"]:
            ex, ey = {"left": (0, 0.5), "right": (1, 0.5), "top": (0.5, 0), "bottom": (0.5, 1)}[hn["arrow"]]
        else:
            dx, dy = hn["tcx"] - bcx, hn["tcy"] - bcy
            if abs(dx) >= abs(dy):
                ex, ey = (1 if dx >= 0 else 0), 0.5
            else:
                ex, ey = 0.5, (1 if dy >= 0 else 0)
        for tid in hn["targets"]:
            t = nodes.get(tid)
            if not t:
                continue
            bx, by = bcx - (t["x"] + t["width"] / 2), bcy - t["cy"]   # target -> box: entry faces the box
            if abs(bx) >= abs(by):
                en, eny = (1 if bx >= 0 else 0), 0.5
            else:
                en, eny = 0.5, (1 if by >= 0 else 0)
            st = (f"edgeStyle=none;html=0;strokeColor=#000000;strokeWidth=1;startArrow=none;endArrow=block;endFill=1;"
                  f"curved=1;exitX={ex};exitY={ey};exitDx=0;exitDy=0;entryX={en};entryY={eny};entryDx=0;entryDy=0;")
            sb.append(f'<mxCell id="a_{hn["id"]}_{tid}" parent="1" edge="1" source="{hn["id"]}" target="{tid}" '
                      f'style="{st}"><mxGeometry relative="1" as="geometry"/></mxCell>')

    sb.append("</root></mxGraphModel></diagram></mxfile>")

    drawio = os.path.join(drawio_dir, f"{lang}.drawio")
    with open(drawio, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(sb) + "\n")
    svg = os.path.join(drawio_dir, f"{lang}.drawio.svg")
    if os.path.exists(svg):
        os.remove(svg)
    subprocess.run([args.drawio_cli, "-x", "-f", "svg", "-e", "-u", "--svg-theme", "auto",
                    "-o", svg, drawio], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(20):                       # the CLI may return just before the file lands
        if os.path.exists(svg):
            break
        time.sleep(0.25)
    if os.path.exists(svg):
        tt = open(svg, encoding="utf-8").read()
        tt = tt.replace("background: transparent; background-color: transparent;",
                        "background: #ffffff; background-color: light-dark(#ffffff, #121212);")
        with open(svg, "w", encoding="utf-8", newline="") as f:
            f.write(tt)
        print(f"  {lang} -> {lang}.drawio.svg ({os.path.getsize(svg)} bytes)")
    else:
        print(f"  {lang} EXPORT FAILED")


def main():
    ap = argparse.ArgumentParser(description="Generate the roadmap draw.io maps from the DSL.")
    ap.add_argument("--dir", required=True, help="folder with structure.dsl + <lang>.tsv")
    ap.add_argument("--langs", default="en,ru,zh", help="comma-separated languages")
    ap.add_argument("--outdir", default=None, help="output dir (defaults to --dir)")
    ap.add_argument("--drawio-cli", default=os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "draw.io", "draw.io.exe"))
    ap.add_argument("--font", default=None, help="path to the metrics font (default: YaHei / Noto CJK)")
    ap.add_argument("--font-family", default="Microsoft YaHei", help="fontFamily written into the map")
    args = ap.parse_args()

    args.outdir = args.outdir or args.dir
    os.makedirs(args.outdir, exist_ok=True)
    if not os.path.exists(args.drawio_cli):
        sys.exit(f"draw.io CLI not found: {args.drawio_cli} (override with --drawio-cli)")
    struct = os.path.join(args.dir, "structure.dsl")
    if not os.path.exists(struct):
        sys.exit(f"structure.dsl not found in {args.dir}")
    font_path = args.font or next((p for p in FONT_CANDIDATES if os.path.exists(p)), None)
    if not font_path:
        sys.exit("no metrics font found (pass --font <path to a .ttf/.ttc>)")
    measure = make_measure(font_path)

    dsl = parse_dsl(struct)
    chrome = load_chrome(os.path.join(args.dir, "chrome.tsv"))
    langs = [x for tok in args.langs.split(",") for x in [tok.strip()] if x]
    print(f"mapgen: {args.dir}")
    for lang in langs:
        build_lang(lang, dsl, chrome, args, measure, args.outdir)
    print("done")


if __name__ == "__main__":
    main()
