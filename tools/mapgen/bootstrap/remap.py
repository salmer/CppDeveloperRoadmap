#!/usr/bin/env python3
"""
remap — re-key a language map onto a reference map's ids.

Some maps were drawn with independent draw.io ids: the same numeric id means a
different node than in the reference map (RU vs EN/ZH — see README, "Cross-language
id alignment"). This tool aligns the target tree to the reference tree structurally
and rewrites the target's `<lang>.tsv` so it is keyed to the *reference* ids, i.e.
drop-in for the canonical `structure.dsl`.

Alignment: both maps reconstruct to the same rooted tree (`extract.build_tree`).
The trees are isomorphic (same roadmap), so children are paired in (y,x) order.
Three independent checks guard correctness:
  - topology  — child counts must match at every node (else the trees aren't
                isomorphic and pairing is unsafe; the run aborts and lists the spots);
  - grade     — paired nodes should share a grade/colour (reported; a signal that is
                independent of tree position);
  - (semantic — paired texts are translations of each other; eyeball the .remap.tsv).
Hints (pink boxes) are matched by their translated target-set, falling back to a
shared id.

Usage:
  python tools/mapgen/bootstrap/remap.py --ref English/Graph/roadmap.drawio.svg \
      --target Russian/Graph/roadmap.drawio.svg -o tools/mapgen/roadmap --lang ru
"""
import argparse, os, sys
from extract import (load, build_tree, GRADE, HINT_FILL, stage_labels,
                     chrome_cells, match_chrome_by_position, load_chrome)

def kids_ordered(verts, kids, nid):
    return sorted(kids[nid], key=lambda n: (verts[n]["y"], verts[n]["x"]))

def align(rv, rk, tv, tk, r_id, t_id, remap, mism):
    """Pair reference node r_id with target node t_id and recurse over ordered kids."""
    remap[t_id] = r_id
    rc = kids_ordered(rv, rk, r_id)
    tc = kids_ordered(tv, tk, t_id)
    if len(rc) != len(tc):
        mism.append((r_id, t_id, len(rc), len(tc)))
    for a, b in zip(rc, tc):            # common prefix still pairs on a mismatch
        align(rv, rk, tv, tk, a, b, remap, mism)

def hint_targets(verts, edges, tree):
    """Pink boxes with >=1 arrow (curved or straight) into the tree — same definition as
    extract.py, so the emitted key set matches the reference `structure.dsl` (orphan notes
    with no in-tree target are not hints)."""
    out = {}
    for hid, v in verts.items():
        if v["fill"] != HINT_FILL: continue
        tg = {e["t"] for e in edges if e["s"] == hid and e["t"] in tree}
        if tg: out[hid] = tg
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", required=True, help="reference map (canonical ids), e.g. English/Graph/roadmap.drawio.svg")
    ap.add_argument("--target", required=True, help="map to re-key, e.g. Russian/Graph/roadmap.drawio.svg")
    ap.add_argument("-o", "--out", required=True, help="output dir (writes <lang>.tsv + <lang>.remap.tsv)")
    ap.add_argument("--lang", default=None, help="tsv basename (default: from the target map's parent dir)")
    ap.add_argument("--words", default=None,
                    help="key the output tsv by the word-ids in this words.tsv instead of ref numeric ids")
    ap.add_argument("--chrome", default=None,
                    help="also emit chrome text, matched to the roles in this chrome.tsv by position")
    ap.add_argument("--center", default="12"); ap.add_argument("--left", default="13"); ap.add_argument("--right", default="14")
    args = ap.parse_args()
    C, L, Rt = args.center, args.left, args.right
    lang = args.lang or os.path.normpath(args.target).split(os.sep)[-3][:2].lower()
    n2w = {}                                   # ref numeric id -> word-id (identity if no --words)
    if args.words:
        for ln in open(args.words, encoding="utf-8"):
            if "\t" in ln and not ln.startswith("#"):
                w, n = ln.rstrip("\n").split("\t", 1); n2w[n] = w
    outkey = lambda r_id: n2w.get(r_id, r_id)

    rv, re_ = load(args.ref);    rpar, rdep, rk = build_tree(rv, re_, C, L, Rt)
    tv, te_ = load(args.target); tpar, tdep, tk = build_tree(tv, te_, C, L, Rt)

    remap, mism = {C: C}, []
    align(rv, rk, tv, tk, L, L, remap, mism)
    align(rv, rk, tv, tk, Rt, Rt, remap, mism)

    if mism:
        print(f"ABORT: {len(mism)} child-count mismatch(es) — trees not isomorphic, pairing unsafe:")
        for r_id, t_id, rc, tc in mism:
            print(f"  ref[{r_id}] {rv[r_id]['text'][:30]!r} has {rc} kids; target[{t_id}] {tv[t_id]['text'][:30]!r} has {tc}")
        return 1

    # independent check: grades should agree
    g = lambda f: GRADE.get(f, "?")
    gmm = [(t, r) for t, r in remap.items() if g(rv[r]["fill"]) != g(tv[t]["fill"])]

    # hints: match by translated target-set. Several hints can share one target
    # (e.g. two notes on node 243), so group by target-set and pair group members in
    # (y,x) order; fall back to a shared id when the target-set itself differs.
    rh, th = hint_targets(rv, re_, set(rpar)), hint_targets(tv, te_, set(tpar))
    yx = lambda V, h: (V[h]["y"], V[h]["x"])
    ref_groups = {}
    for h in sorted(rh, key=lambda h: yx(rv, h)):
        ref_groups.setdefault(frozenset(rh[h]), []).append(h)
    tgt_groups = {}
    for h in sorted(th, key=lambda h: yx(tv, h)):
        tgt_groups.setdefault(frozenset(remap.get(t) for t in th[h]), []).append(h)
    hint_remap, hint_unmatched = {}, []
    for key, ths in tgt_groups.items():
        refs = ref_groups.get(key, [])
        for i, t_hid in enumerate(ths):
            if i < len(refs): hint_remap[t_hid] = refs[i]
            elif t_hid in rh: hint_remap[t_hid] = t_hid       # shared-id fallback
            else: hint_unmatched.append(t_hid)

    # emit <lang>.tsv keyed to REF ids (or word-ids via --words), mirroring extract.py's
    # order (center, pre-order, hints)
    r2t = {r: t for t, r in remap.items()}
    rows = [f"{outkey(C)}\t{tv[C]['text']}"]
    def walk(r_id):
        rows.append(f"{outkey(r_id)}\t{tv[r2t[r_id]]['text']}")
        for c in kids_ordered(rv, rk, r_id): walk(c)
    for root in sorted([L, Rt], key=lambda r: rv[r]["y"]): walk(root)
    rh2t = {r: t for t, r in hint_remap.items()}
    for r_hid in sorted(rh, key=lambda h: (rv[h]["y"], rv[h]["x"])):
        if r_hid in rh2t: rows.append(f"{outkey(r_hid)}\t{tv[rh2t[r_hid]]['text']}")
    rows += [f"stage{n}\t{lab}" for n, lab in sorted(stage_labels(tv).items())]   # target's stage titles
    if args.chrome:   # RU chrome ids diverged but its layout is preserved -> match by position
        ct = match_chrome_by_position(load_chrome(args.chrome), chrome_cells(tv, set(tpar)))
        rows += [f"{role}\t{text}" for role, text in ct.items()]

    os.makedirs(args.out, exist_ok=True)
    open(os.path.join(args.out, f"{lang}.tsv"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
    qual = lambda p: "/".join(os.path.normpath(p).split(os.sep)[-3:])
    prov = [f"# target_id\tref_id  (re-key of {qual(args.target)} onto {qual(args.ref)})"]
    prov += [f"{t}\t{r}" for t, r in sorted(remap.items(), key=lambda kv: (len(kv[1]), kv[1]))]
    open(os.path.join(args.out, f"{lang}.remap.tsv"), "w", encoding="utf-8").write("\n".join(prov) + "\n")

    changed = sum(1 for t, r in remap.items() if t != r)
    print(f"aligned {len(remap)} nodes (0 topology mismatches), {changed} ids re-keyed")
    print(f"grade agreement: {len(remap)-len(gmm)}/{len(remap)} (mismatches: {len(gmm)})")
    for t, r in gmm[:10]:
        print(f"  grade differs: ref[{r}] {g(rv[r]['fill'])} {rv[r]['text'][:22]!r} vs target[{t}] {g(tv[t]['fill'])}")
    print(f"hints: {len(hint_remap)}/{len(th)} mapped" + (f", UNMATCHED {hint_unmatched}" if hint_unmatched else ""))
    print(f"wrote {args.out}/{lang}.tsv and {lang}.remap.tsv")
    return 0

if __name__ == "__main__":
    sys.exit(main())
