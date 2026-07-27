# Notes for AI agents: working on the roadmap

This file helps an AI agent (or a human) get up to speed on the repository quickly: how the
map is produced, how to change it safely, and the conventions to keep.

This is **not a changelog** — for what changed and when, see the git history; the owner's
current tasks live in [TODO.md](TODO.md).

> **IMPORTANT: the maps are GENERATED, not hand-edited.**
> Each `<Language>/Graph/roadmap.drawio.svg` is **build output** of the mapgen pipeline.
> Do not edit those files (or their embedded draw.io XML) directly — edit the source in
> [`tools/mapgen/roadmap/`](tools/mapgen/roadmap) and rebuild. CI (`mapcheck`) fails if a
> committed map no longer matches the source, so hand-edits will not pass.

## Repository conventions

- **Commit messages: English only.** Article and map content is maintained in
  Russian/English/Chinese, but the git history is English.
- `main` is the primary branch; work through separate branches and pull requests.
- Article file names and URLs must not change — they are linked from outside.
- **Articles** (the per-language `.md` content) are still maintained by hand, one copy per
  language; any content change must be mirrored across `English/` `Russian/` `Chinese/`
  (there is no `Spanish/` yet). **The map is different** — it has a single source (below),
  so a structural change is made once and regenerated into every language.

## How the map is produced

```
tools/mapgen/roadmap/structure.dsl  +  <lang>.tsv   ──►  build.py  ──►  <lang>.drawio.svg
        (one language-neutral source)   (per-lang text)  (layout engine)  (copied to <Language>/Graph/)
```

- **`structure.dsl`** fixes the *logical* map: the node tree (indentation = hierarchy), each
  node's grade (colour) and maturity `stage`, the pink hint boxes (`angle`/`dist`/`arrow`),
  the spine, and the stage frames. Language-neutral **word-ids** (`[standard-library-stl]`)
  are the shared key.
- **`<lang>.tsv`** is `id <TAB> text` — only the words, per language. Chrome (title, legend,
  About/date) text lives here too, keyed by role; its geometry is in `chrome.tsv`.
- **`build.py`** computes the *physical* layout (widths from text metrics, packing, routing,
  frame growth) and renders via the draw.io CLI. Output is byte-for-byte reproducible from
  the source. Full grammar and build/flags: [`tools/mapgen/README.md`](tools/mapgen/README.md).
- Each language's map is still a single `<Language>/Graph/roadmap.drawio.svg` — an SVG image
  with the draw.io source embedded in the `content` attribute of the root `<svg>`. That's the
  **output**; treat it as generated.

## Editing the map

1. Edit the source in `tools/mapgen/roadmap/`:
   - **structure / grade / stage / hint placement** → `structure.dsl`
   - **text** (a label, a hint's wording, the date, a legend caption) → the relevant
     `<lang>.tsv` row(s). A structural add needs a new row in **all three** tsvs.
2. Rebuild and copy over the live maps:
   ```bash
   pip install -r tools/mapgen/requirements.txt      # first time (Pillow)
   python tools/mapgen/build.py --dir tools/mapgen/roadmap --langs en,ru,zh
   cp tools/mapgen/roadmap/en.drawio.svg English/Graph/roadmap.drawio.svg
   cp tools/mapgen/roadmap/ru.drawio.svg Russian/Graph/roadmap.drawio.svg
   cp tools/mapgen/roadmap/zh.drawio.svg Chinese/Graph/roadmap.drawio.svg
   ```
   (needs the draw.io desktop CLI at `%LOCALAPPDATA%\Programs\draw.io\`; `--drawio-cli` to override.)
3. Validate: `python tools/mapcheck/check.py --no-date` must report **0 hard errors**.
4. Commit the changed source **and** the regenerated maps together.

Reverse-engineering an existing map back into the DSL, and onboarding a new language, are
one-off jobs handled by [`tools/mapgen/bootstrap/`](tools/mapgen/bootstrap) — not part of the
normal edit loop.

## Conventions the generator follows (and you should preserve in the DSL)

- **Colour legend** (grades → fillColor): junior `#96BB7C`, middle `#FAD586`, senior
  `#BBCCEE`, optional `#CCEEFF`; pink hints `#FFD5E4`, grey stage frames `#F5F5F5`, centre
  node `#FFE5B9`, chrome body `#FFF5EB`. Set a node's grade in the DSL, not a colour.
- **The "Last updated" date** is a `<lang>.tsv` entry (role `last-updated`,
  "Last updated: YYYY-MM-DD"). Bump it when you change a map — `mapcheck`'s date check warns
  if it predates the map's last commit. Its light `#FFF5EB` fill is deliberate: black text on
  a bare background is invisible in the map's dark theme.
- **Stage frames** grow to fit their `(section, stage)` group automatically; the "N step"
  titles come from the `stage1`..`stage5` tsv keys. Just annotate a subtree root with `stage=N`.
- **Hints** are placed by explicit polar `angle`/`dist` from their target and a required
  `arrow=` side; one value serves all three languages, so re-check `mapcheck` after moving one.
- Rows share `y` across languages (`PITCH=60`, box `H=30`); only x/width differ per language.
  The generator handles this — you don't port vertical positions by hand any more.

## Validation — `tools/mapcheck`

`check.py` runs in CI on every PR touching a map ([`.github/workflows/map-check.yml`](.github/workflows/map-check.yml))
and scans all `<Language>/Graph/roadmap.drawio.svg`. Hard errors (fail CI): box-fits-text
(Latin), overlaps, and **map-vs-DSL** (a committed map that no longer matches
`tools/mapgen/roadmap` — ids, grades, `<lang>.tsv` text, or a missing translation). Warnings:
cross-language drift and a stale date. See [`tools/mapcheck/README.md`](tools/mapcheck/README.md).

## Open questions

- **The fate of Miro.** The Miro boards (external) don't sync with draw.io and have fallen
  behind; they are marked obsolete in every language's README. Optional plan: check
  GoatCounter traffic for `/goto/miro-*` vs `/goto/svg-*`; if low, put a "the map has moved"
  banner on the boards and redirect `goto/miro` to the SVG viewer (without breaking links).
- **The owner's current tasks are in [TODO.md](TODO.md)**; check it directly.
