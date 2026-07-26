# mapgen — generate draw.io map fragments from a text DSL + translations

The roadmap map is maintained as a rigid text source plus per-language translation files,
with draw.io as the output format.

**Layout.** `roadmap/` holds the **real map source** — `structure.dsl` + `en/ru/zh.tsv` +
`chrome.tsv` + `words.tsv`. `build.py` turns it into `roadmap/<lang>.drawio.svg` (a
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
structure.dsl  +  <lang>.tsv  ──►  build.py  ──►  <lang>.drawio  ──►  draw.io CLI  ──►  <lang>.drawio.svg
                                   (layout engine)                    (-x -f svg -e)     (+ bg restore)
```

The DSL fixes the **logical** layout (rows, order, grade, stage, hint targets, spine
sides). The generator computes the **physical** layout:

- **width** = measured text width (Pillow, the same library mapcheck uses) + padding, per language;
- **packing** — local: each child sits just right of its own parent (the left half
  mirrors, packing left), with a vertical bus in the gap carrying the parent→child edges;
  rows share `y` across languages (`PITCH=60`, box `H=30`);
- **hints** — wrapped to a fixed width and placed at an explicit polar offset (`angle`,
  `dist`) from their target; positions are authored in the DSL, not auto-laid-out;
- **frames** — grow to the bounding box of their members + a title band;
- **spine** — a central trunk the section roots hang off, both halves centred on the
  `center` node; hub-x is computed from the left half's width, so it shifts per language.

## Usage

Requires **Python 3 + Pillow** (`pip install -r tools/mapgen/requirements.txt`, or just
`pip install Pillow` — note the package is `Pillow`, imported as `PIL`) and the **draw.io
desktop CLI** (`%LOCALAPPDATA%\Programs\draw.io\draw.io.exe`).

```bash
pip install -r tools/mapgen/requirements.txt
python tools/mapgen/build.py --dir tools/mapgen/roadmap --langs en,ru,zh
```

`--dir` holds `structure.dsl` and one `<lang>.tsv` per language. Output `<lang>.drawio` +
`<lang>.drawio.svg` land next to them (override with `--outdir`), then copy the
`<lang>.drawio.svg` over the live `<Lang>/Graph/roadmap.drawio.svg`. It's a real draw.io
file — open it in draw.io to inspect, but edits there are lost on regeneration (see Caveats).

Flags: `--langs en,ru,zh`, `--outdir <dir>`, `--drawio-cli <path>`, `--font <path>` (metrics
font, default `msyh.ttc` / Noto CJK), `--font-family "<name>"` (written into the map).

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

### Hints — `hint [id] angle=<deg> dist=<px> arrow=<side> -> target, target, ...`

A pink annotation box, text from `<lang>.tsv` (auto-wrapped, CJK-aware), with a curved
arrow to each target. The box is placed at a **polar offset** from the mean target centre:
`angle` degrees (0 = right, 90 = up) and `dist` pixels. Example:

```
hint [choose-one-of-the] angle=175 dist=419 arrow=right -> windbg, gdb, lldb
```

`arrow=left|right|top|bottom` is **required** — it sets which box edge the arrow **starts**
from (e.g. a note above its target uses `arrow=bottom`). The arrow always ends on the target
edge facing the box. `extract.py` seeds it from the box's position (the edge facing the
target); the build fails if any hint omits it.

Placement is **explicit, not auto-laid-out** — the generator just puts the box where the
coords say. The initial `angle`/`dist` were seeded from the hand map during bootstrap, so
the notes replay in their hand-tuned positions; you nudge the values by hand in
`structure.dsl` (the source of truth) when a note needs to move. Rows are shared across languages so an offset
transfers; only the target's x shifts with per-language width, carrying the box along.
Because box heights and node widths differ per language, one `angle`/`dist` has to clear
all three — nudge the values until `mapcheck` reports no overlaps. If omitted, the box
defaults to straight right of its target (`angle=0`), with no overlap avoidance.

### Stage frames — automatic from `stage=`

Nodes carrying a `stage=N` (inherited by the subtree) are wrapped in a grey `#F5F5F5`
box grown to fit, one per **(section, stage)** group — the same banding the hand-drawn
map uses. Titles come from the `stage1`..`stage5` tsv keys (`1 step` / `1 этап` / `步骤 1`).
A gap is inserted between stage bands so the boxes don't touch. No directive is needed —
just annotate the subtree roots.

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

## Translation files `<lang>.tsv`

One `id <TAB> text` per line, UTF-8 (no BOM). A missing id falls back to the id itself.
Keys include node ids, chrome roles, and any `frame` title / `spine` header keys.

## Bootstrapping the source

`roadmap/` was reverse-engineered from the original hand-drawn maps — the EN map becomes the
word-id `structure.dsl` + `en.tsv` + `words.tsv` + `chrome.tsv`; ZH and RU are keyed onto the
same word-ids. That's a one-off; the tools live in [`bootstrap/`](bootstrap/README.md) and
are also how a new language is onboarded. **Going forward the DSL is the source — edit
`structure.dsl` / `<lang>.tsv` directly, never re-derive from a generated map.**

For reference, `roadmap/` holds the canonical `structure.dsl` (394 nodes + 34 hints + 25
stage annotations), `chrome.tsv` (18 static blocks: title, legend, About/How-to/Feedback,
repo link, date), `en/ru/zh.tsv`, `words.tsv`, and `ru.remap.tsv` (RU-numeric → word-id
provenance from the re-key).

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
- **Metrics font.** Text is measured with Pillow using `Microsoft YaHei` (Latin+Cyrillic+CJK;
  falls back to Noto CJK) while draw.io renders Latin in Helvetica, so generated widths aren't
  pixel-identical to what draw.io lays out — mapcheck's relative margin absorbs the difference.
  The draw.io CLI path defaults to the Windows install; pass `--drawio-cli` elsewhere.

See [AGENTS.md](../../AGENTS.md) for the map conventions this tool mirrors (row pitch,
stage-frame title band, gate/hub-x, colour legend).
