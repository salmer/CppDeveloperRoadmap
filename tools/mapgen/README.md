# mapgen — generate draw.io map fragments from a text DSL + translations

**Status: prototype / proof-of-concept.** This is a feasibility spike, not yet wired
into the map build. It shows that the roadmap map can be maintained as a rigid text
source plus per-language translation files, with draw.io as the output format.

## Why

The map lives as three hand-maintained `.drawio.svg` files (RU/EN/ZH, soon +ES). Two
recurring pains:

- **Sync drift** — structural edits must be ported RU→EN→ZH by hand (see
  [AGENTS.md](../../AGENTS.md), "Porting edits between languages").
- **Language-dependent width** — the same node is a different width per language, so
  positions can't simply be shared; a box that fits EN can clip ZH (the "C++26 box too
  narrow" class of bug).

Idea: keep **one** language-neutral structure, put the text in **per-language files**,
and **generate** the draw.io per language. The structure is fixed rigidly; only the
physical layout (x, width, routing, frame size) is computed per language.

## How it works

```
structure.dsl  +  <lang>.tsv  ──►  build.ps1  ──►  <lang>.drawio  ──►  draw.io CLI  ──►  <lang>.drawio.svg
                                   (layout engine)                     (-x -f svg -e)     (+ bg restore)
```

The DSL fixes the **logical** layout (rows, columns, order, grade, hint/frame anchors,
spine). The generator computes the **physical** layout:

- **width** = measured text width (System.Drawing) + padding, per language;
- **columns** — one per depth; column width = widest node in it; a vertical bus runs in
  the gap between columns; rows share `y` across languages (`PITCH=60`, box `H=30`);
- **hints** — wrapped to a fixed width and pushed right until they clear **every** node
  whose vertical span overlaps the box (2D clearance);
- **frames** — grow to the bounding box of their members + a title band;
- **spine** — a fixed trunk at `hub-x`; section roots hang off it; a header sits left of
  `gate`. With `hub-x`/`gate` held constant, everything left of the gate stays put while
  the right half reflows per language.

## Usage

Requires **Windows** (System.Drawing metrics) and the **draw.io desktop CLI**
(`%LOCALAPPDATA%\Programs\draw.io\draw.io.exe`).

```powershell
pwsh tools/mapgen/build.ps1 -Dir tools/mapgen/examples/stl
pwsh tools/mapgen/build.ps1 -Dir tools/mapgen/examples/debugger
pwsh tools/mapgen/build.ps1 -Dir tools/mapgen/examples/libraries
pwsh tools/mapgen/build.ps1 -Dir tools/mapgen/examples/spine -Langs en,ru,zh
```

Each `-Dir` holds `structure.dsl` and one `<lang>.tsv` per language. Output
`<lang>.drawio` + `<lang>.drawio.svg` land next to them (override with `-OutDir`). The
`.drawio.svg` is a real draw.io file — open and edit it in draw.io.

Flags: `-Langs en,ru,zh`, `-OutDir <dir>`, `-DrawioCli <path>`, `-Font "<name>"`.

## DSL grammar

A line-based text format. `#` starts a comment. Blank lines ignored.

### Nodes (indentation = hierarchy, 2 spaces per level)

```
[basic-operations] grade=junior stage=1
  [arithmetic-operations] grade=optional
    [loops-for-while] grade=middle
```

- `[id]` — a **word-id** (a short slug of the English name, e.g. `standard-library-stl`),
  stable and language-neutral; the display text comes from `<lang>.tsv` (`id <TAB> text`).
  Word-ids are the same key in every language, so translations can't drift apart the way
  the maps' native numeric draw.io ids did (see "Cross-language id alignment").
- `grade` — colour class: `junior` `#96BB7C`, `middle` `#FAD586`, `senior` `#BBCCEE`,
  `optional` `#CCEEFF` (matches the map legend). Defaults to `junior`.
- `stage` — maturity band (1–5), inherited by the subtree (like `side`). Consecutive
  same-stage subtrees within a section are wrapped by a grow-to-fit stage frame. Only the
  shallowest node of each band needs the annotation.
- Depth 0 nodes are roots (columns pack rightward from there).

### Hints — `hint [id] -> target, target, ...`

A pink annotation box, text from `<lang>.tsv` (auto-wrapped, CJK-aware). Drawn right of
its targets with a curved arrow to each. Example:

```
hint [choose-one-of-the] -> windbg, gdb, lldb
```

### Stage frames — automatic from `stage=`

Nodes carrying a `stage=N` (inherited by the subtree) are wrapped in a grey `#F5F5F5`
box grown to fit, one per **(section, stage)** group — the same banding the hand-drawn
map uses. Titles come from the `stage1`..`stage5` tsv keys (`1 step` / `1 этап` / `步骤 1`),
which `extract.py` reads from the map's frames. A gap is inserted between stage bands so
the boxes don't touch. No directive is needed — just annotate the subtree roots.

### Explicit frames — `frame [id] title=<key> [contains=a,b]`

A box drawn behind the nodes, grown to fit. `title` is a translation key. Without
`contains`, it encloses everything; with it, only those roots' subtrees.

```
frame [libs] title=libraries contains=boost,opencv
```

### Spine — `spine [center=<id>] [hubx=<x>] [gate=<x>] [header=<key>]`

A central trunk; depth-0 nodes become sections hanging off it. Each root is placed on a
side with `side=left|right` (inherited by its subtree, default `right`): the right half
packs rightward from the trunk, the left half packs leftward (mirror). Nodes use **local
packing** — each child sits just right of its own parent — so deep trees stay compact.

- **`center=<id>`** puts a node on the trunk at the vertical middle and centres both halves
  on it (the "C++ developer" node the two halves emanate from). The two halves stack
  top-down in parallel.
- **hub-x is computed** from the left half's actual width when `hubx` is omitted — wider
  labels in one language push the whole centre right, per language. Pass `hubx` to pin it.
- Optional `gate`/`header` draw a dashed gate guide + a left-of-gate header.

```
spine center=12             # bilateral, centre node, computed hub-x
[13] side=left              # Soft skills
  [21]                      # Communication ...
[14] side=right             # Hard skills
  [396]                     # Language syntax ...

spine hubx=460 gate=420 header=hardskills   # pinned hub-x + gate guide (right side only)
```

## Extracting a DSL from an existing map

`extract.py` reverses a `roadmap.drawio.svg` into `structure.dsl` + `<lang>.tsv` (BFS tree
from the centre/left/right anchors, grades from fill, `stage` from the `#F5F5F5` frames,
pink boxes → hints; handles link-bearing `UserObject` nodes).

The canonical structure is built from the **EN** map with `--slugs`, which assigns the
word-ids and writes a `words.tsv` bridge (word → EN numeric id). Other languages are then
keyed to those same word-ids — ZH shares EN's numeric ids so it is relabelled directly;
RU used independent ids so it goes through `remap.py` (below):

```bash
# reference: word-id structure.dsl + en.tsv + words.tsv + chrome.tsv (+ stage annotations)
python tools/mapgen/extract.py English/Graph/roadmap.drawio.svg -o examples/fullmap --lang en --slugs
# ZH shares EN's ids -> relabel text (--words) + match chrome by id (--chrome)
python tools/mapgen/extract.py Chinese/Graph/roadmap.drawio.svg -o examples/fullmap --lang zh --words examples/fullmap/words.tsv --chrome examples/fullmap/chrome.tsv
# RU diverged -> align + key by word (--words) + match chrome by position (--chrome)
python tools/mapgen/remap.py --ref English/Graph/roadmap.drawio.svg --target Russian/Graph/roadmap.drawio.svg -o examples/fullmap --lang ru --words examples/fullmap/words.tsv --chrome examples/fullmap/chrome.tsv
```

`examples/fullmap` holds one canonical word-id `structure.dsl` (394 nodes + 28 hints + 25
stage annotations), the `chrome.tsv` layout (18 static blocks: title, legend,
About/How-to/Feedback, repo link, date), `en.tsv`/`zh.tsv`/`ru.tsv` (all keyed by the same
word-ids and chrome roles) and `words.tsv`. **Chrome text** is matched to the reference
roles by draw.io id for ZH (shares ids) and by position for RU (ids diverged, layout kept).

**Cross-language id alignment (measured by extracting all three maps).** Word-ids are the
shared key now; this is *why* they were needed:

- **EN and ZH share the draw.io id scheme** — identical topology and grades for every
  shared id; ZH only lacks two nodes EN has (`n922`, `n923`). So ZH text maps straight onto
  the word-ids via `words.tsv`.
- **RU used independent ids** — the same numeric id mapped to a *different* node than in
  EN/ZH (e.g. id `354` is "Process" in EN but "Асинхронные" in RU's own map). `remap.py`
  (below) aligns RU to EN structurally and keys its text by word-id. `ru.remap.tsv` records
  the RU-numeric → EN-numeric mapping it produced.

### Translation files `<lang>.tsv`

One `id <TAB> text` per line, UTF-8 (no BOM). A missing id falls back to the id itself.
Keys include node ids plus any `frame` title / `spine` header keys.

### Re-keying a map onto the canonical ids

When a map was drawn with independent ids (RU), `remap.py` aligns it to a reference map
and rewrites its `<lang>.tsv` to the reference ids — drop-in for the canonical
`structure.dsl`:

```bash
python tools/mapgen/remap.py --ref English/Graph/roadmap.drawio.svg \
    --target Russian/Graph/roadmap.drawio.svg -o tools/mapgen/examples/fullmap --lang ru
```

Both maps reconstruct to the same rooted tree (they describe the same roadmap), so
children are paired in `(y, x)` order. Correctness is cross-checked three ways: **topology**
(child counts must match at every node, else it aborts), **grade** (paired nodes must share
a colour — a signal independent of position; RU came out 395/395), and **semantic** (paired
texts are translations — eyeball `<lang>.remap.tsv`). Hints are matched by their translated
target-set (group-paired in `(y, x)` order when several share a target). The RU re-key ran
clean: 0 topology mismatches, 0 grade mismatches, 28/28 hints, 164 ids re-keyed.

## Examples

| Dir | Demonstrates |
|-----|--------------|
| `examples/stl` | multi-child tree + bus; per-language width (EN/RU/ZH) |
| `examples/debugger` | hint callouts + curved multi-target arrows + 2D clearance |
| `examples/libraries` | frame grow-to-fit, two parents, 3rd-level sub-branches |
| `examples/spine` | pinned trunk (hub-x) + left-of-gate header + right-half reflow |
| `examples/bilateral` | two-sided spine: left mirror + **computed per-language hub-x** |
| `examples/fullmap` | whole map end-to-end: word-id structure + stages + `en`/`zh`/`ru` tsv |

## Known gaps (before this could replace the hand workflow)

1. **Whole map generates.** Skill tree, hints, stage frames (from `stage=`) and the
   top-left chrome — title banner, legend, About/How-to/Feedback, repo link, date — all
   come out of the canonical source. Chrome layout is captured once in `chrome.tsv`
   (language-neutral geometry+style); text is per-language in `<lang>.tsv`. The one thing
   still hand-verified is that the tree's own gaps match the original closely enough.
2. **All three languages are now on one canonical `structure.dsl`.** EN and ZH share
   draw.io ids natively; RU is re-keyed by `remap.py` (validated clean). Remaining content
   drift: ZH lacks two nodes EN has (`n922`, `n923`) — those fall back to id text until ZH
   gains them.
3. **No round-trip.** draw.io stays the *output*; hand-edits to a generated file are lost
   on regeneration. Discipline: structure in `structure.dsl`, text in `<lang>.tsv`, never
   hand-edit the generated `.drawio.svg`.
4. **Hardening.** Not yet run on all 457 nodes; needs stable output ordering (clean
   diffs), error handling, and integration into the repo build.
5. **Platform.** Windows-only today (System.Drawing + draw.io CLI). Text metrics use a
   font that covers Latin+Cyrillic+CJK (default `Microsoft YaHei`); the map itself uses
   Helvetica for Latin, so generated widths won't be pixel-identical to hand-drawn ones.

See [AGENTS.md](../../AGENTS.md) for the map conventions this tool mirrors (row pitch,
stage-frame title band, gate/hub-x, colour legend).
