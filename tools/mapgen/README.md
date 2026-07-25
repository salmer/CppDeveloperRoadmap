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
[id] grade=junior
  [child_id] grade=optional
    [grandchild_id] grade=middle
```

- `[id]` — stable key; the display text comes from `<lang>.tsv` (`id <TAB> text`).
  Ids never change, so they don't diverge across languages the way node ids do today.
- `grade` — colour class: `junior` `#96BB7C`, `middle` `#FAD586`, `senior` `#BBCCEE`,
  `optional` `#CCEEFF` (matches the map legend). Defaults to `junior`.
- Depth 0 nodes are roots (columns pack rightward from there).

### Hints — `hint [id] -> target, target, ...`

A pink annotation box, text from `<lang>.tsv` (auto-wrapped, CJK-aware). Drawn right of
its targets with a curved arrow to each. Example:

```
hint [h_cmdline] -> windbg, gdb, lldb
```

### Frames — `frame [id] title=<key> [contains=a,b]`

A stage box drawn behind the nodes, grown to fit. `title` is a translation key.
Without `contains`, it encloses everything; with it, only those roots' subtrees.

```
frame [f5] title=stage5
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
from the centre/left/right anchors, grades from fill, pink boxes → hints; handles
link-bearing `UserObject` nodes). Run once per language:

```bash
python tools/mapgen/extract.py English/Graph/roadmap.drawio.svg -o tools/mapgen/examples/fullmap
```

`examples/fullmap` is the result for the EN map (394 nodes + 28 hints). Not extracted yet:
stage frames, the legend/title/About blocks, and a handful of isolated nodes.

### Translation files `<lang>.tsv`

One `id <TAB> text` per line, UTF-8 (no BOM). A missing id falls back to the id itself.
Keys include node ids plus any `frame` title / `spine` header keys.

## Examples

| Dir | Demonstrates |
|-----|--------------|
| `examples/stl` | multi-child tree + bus; per-language width (EN/RU/ZH) |
| `examples/debugger` | hint callouts + curved multi-target arrows + 2D clearance |
| `examples/libraries` | frame grow-to-fit, two parents, 3rd-level sub-branches |
| `examples/spine` | pinned trunk (hub-x) + left-of-gate header + right-half reflow |
| `examples/bilateral` | two-sided spine: left mirror + **computed per-language hub-x** |
| `examples/fullmap` | the whole EN map extracted end-to-end (centre node + 394 nodes + hints) |

## Known gaps (before this could replace the hand workflow)

1. **Decorative content not extracted.** The full-map extraction covers the skill tree +
   hints; stage frames, the legend/title/About blocks and ~7 isolated nodes are not yet
   pulled in. RU/ZH need `extract.py` run on their maps (upper-part ids are shared).
2. **No round-trip.** draw.io stays the *output*; hand-edits to a generated file are lost
   on regeneration. Discipline: structure in `structure.dsl`, text in `<lang>.tsv`, never
   hand-edit the generated `.drawio.svg`.
3. **Hardening.** Not yet run on all 457 nodes; needs stable output ordering (clean
   diffs), error handling, and integration into the repo build.
4. **Platform.** Windows-only today (System.Drawing + draw.io CLI). Text metrics use a
   font that covers Latin+Cyrillic+CJK (default `Microsoft YaHei`); the map itself uses
   Helvetica for Latin, so generated widths won't be pixel-identical to hand-drawn ones.

See [AGENTS.md](../../AGENTS.md) for the map conventions this tool mirrors (row pitch,
stage-frame title band, gate/hub-x, colour legend).
