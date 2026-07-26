# mapgen — generate draw.io map fragments from a text DSL + translations

The roadmap map is maintained as a rigid text source plus per-language translation files,
with draw.io as the output format.

**Layout.** `roadmap/` holds the **real map source** — `structure.dsl` + `en/ru/zh.tsv` +
`chrome.tsv` + `words.tsv`. `build.ps1` turns it into `roadmap/<lang>.drawio.svg` (a
gitignored build artifact), which is then copied over the three live maps at
`<Lang>/Graph/roadmap.drawio.svg`. The copy-to-live step is still manual (not yet wired
into CI).

## Why

The map had lived as three hand-maintained `.drawio.svg` files (RU/EN/ZH, soon +ES) — which
mapgen now generates. Two recurring pains motivated the switch:

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

The DSL fixes the **logical** layout (rows, order, grade, stage, hint targets, spine
sides). The generator computes the **physical** layout:

- **width** = measured text width (System.Drawing) + padding, per language;
- **packing** — local: each child sits just right of its own parent (the left half
  mirrors, packing left), with a vertical bus in the gap carrying the parent→child edges;
  rows share `y` across languages (`PITCH=60`, box `H=30`);
- **hints** — wrapped to a fixed width and placed at an explicit polar offset (`angle`,
  `dist`) from their target; positions are authored in the DSL, not auto-laid-out;
- **frames** — grow to the bounding box of their members + a title band;
- **spine** — a central trunk the section roots hang off, both halves centred on the
  `center` node; hub-x is computed from the left half's width, so it shifts per language.

## Usage

Requires **Windows** (System.Drawing metrics) and the **draw.io desktop CLI**
(`%LOCALAPPDATA%\Programs\draw.io\draw.io.exe`).

```powershell
pwsh tools/mapgen/build.ps1 -Dir tools/mapgen/roadmap -Langs en,ru,zh
```

`-Dir` holds `structure.dsl` and one `<lang>.tsv` per language. Output `<lang>.drawio` +
`<lang>.drawio.svg` land next to them (override with `-OutDir`), then copy the
`<lang>.drawio.svg` over the live `<Lang>/Graph/roadmap.drawio.svg`. It's a real draw.io
file — open it in draw.io to inspect, but edits there are lost on regeneration (see Caveats).

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
- Depth-0 nodes are section roots (placed on the spine — see below).

### Hints — `hint [id] angle=<deg> dist=<px> -> target, target, ...`

A pink annotation box, text from `<lang>.tsv` (auto-wrapped, CJK-aware), with a curved
arrow to each target. The box is placed at a **polar offset** from the mean target centre:
`angle` degrees (0 = right, 90 = up) and `dist` pixels. Example:

```
hint [choose-one-of-the] angle=175 dist=419 -> windbg, gdb, lldb
```

Placement is **explicit, not auto-laid-out** — the generator just puts the box where the
coords say. `extract.py` fills `angle`/`dist` from the hand map, so the notes replay in
their hand-tuned positions; you then nudge the values by hand in `structure.dsl` (the
source of truth) when a note needs to move. Rows are shared across languages so an offset
transfers; only the target's x shifts with per-language width, carrying the box along.
Because box heights and node widths differ per language, one `angle`/`dist` has to clear
all three — nudge the values until `mapcheck` reports no overlaps. If omitted, the box
defaults to straight right of its target (`angle=0`), with no overlap avoidance.

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
spine center=cpp-developer     # bilateral, centre node, computed hub-x
[soft-skills] side=left
  [ability-to-learn]           # subtree inherits side=left
[hard-skills] side=right
  [language-syntax]            # subtree inherits side=right

spine hubx=460 gate=420 header=hardskills   # optional: pinned hub-x + dashed gate guide
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
python tools/mapgen/extract.py English/Graph/roadmap.drawio.svg -o roadmap --lang en --slugs
# ZH shares EN's ids -> relabel text (--words) + match chrome by id (--chrome)
python tools/mapgen/extract.py Chinese/Graph/roadmap.drawio.svg -o roadmap --lang zh --words roadmap/words.tsv --chrome roadmap/chrome.tsv
# RU diverged -> align + key by word (--words) + match chrome by position (--chrome)
python tools/mapgen/remap.py --ref English/Graph/roadmap.drawio.svg --target Russian/Graph/roadmap.drawio.svg -o roadmap --lang ru --words roadmap/words.tsv --chrome roadmap/chrome.tsv
```

`roadmap` holds one canonical word-id `structure.dsl` (394 nodes + 34 hints + 25
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
    --target Russian/Graph/roadmap.drawio.svg -o tools/mapgen/roadmap --lang ru
```

Both maps reconstruct to the same rooted tree (they describe the same roadmap), so
children are paired in `(y, x)` order. Correctness is cross-checked three ways: **topology**
(child counts must match at every node, else it aborts), **grade** (paired nodes must share
a colour — a signal independent of position; RU came out 395/395), and **semantic** (paired
texts are translations — eyeball `<lang>.remap.tsv`). Hints are matched by their translated
target-set (group-paired in `(y, x)` order when several share a target). The RU re-key ran
clean: 0 topology mismatches, 0 grade mismatches, 34/34 hints, 164 ids re-keyed.

## What generates

The whole map, all three languages, from the canonical source: skill tree, hints, stage
frames (from `stage=`), and the top-left chrome — title banner, legend,
About/How-to/Feedback, repo link, date. Chrome layout is captured once in `chrome.tsv`
(language-neutral geometry + style); text is per-language in `<lang>.tsv`. RU is re-keyed
onto EN's word-ids by `remap.py` (validated clean); EN and ZH share ids natively. Validated
by `mapcheck` (457 vertices, box-fits-text + overlaps + cross-language drift).

## Caveats & remaining work

- **No round-trip.** draw.io stays the *output*; hand-edits to a generated `.drawio.svg`
  are lost on regeneration. Edit `structure.dsl` / `<lang>.tsv`, never the output.
- **Not automated.** The copy-to-live step is manual and there's no CI check yet; the
  AGENTS.md hand-porting workflow hasn't been updated to point here.
- **Per-language hint tuning.** One `angle`/`dist` per hint must clear all three languages
  (see the Hints section).
- **ZH content drift.** ZH lacks two nodes EN has (`n922`, `n923`); they fall back to id
  text until ZH gains them.
- **Platform.** Windows-only (System.Drawing + draw.io CLI). Metrics use `Microsoft YaHei`
  (Latin+Cyrillic+CJK) while the hand maps use Helvetica for Latin, so generated widths
  aren't pixel-identical to the originals.

See [AGENTS.md](../../AGENTS.md) for the map conventions this tool mirrors (row pitch,
stage-frame title band, gate/hub-x, colour legend).
