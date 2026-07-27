# mapcheck — validate the roadmap maps

Static checks over `<Lang>/Graph/roadmap.drawio.svg`, run in CI on every PR that
touches a map (`.github/workflows/map-check.yml`). Catches the classes of bug that
have actually bitten this map.

## Checks

| Check | Severity | What it catches |
|-------|----------|-----------------|
| **box-fits-text** | hard (Latin) / warning (CJK) | a node whose label is wider than its box — e.g. the "C++26 (newest)" box that was 73px wide for ~143px of text |
| **overlaps** | hard | two content nodes whose boxes overlap (AGENTS.md requires 0) |
| **map-vs-DSL** | hard | the committed map has drifted from its source `tools/mapgen/roadmap` — a node/hint id, grade, or `<lang>.tsv` text that doesn't match (i.e. the DSL/tsv was edited but the map wasn't rebuilt + copied), or a missing/blank `<lang>.tsv` entry (the box shows the raw word-id, which box-fits and drift can't see) |
| **drift** | warning | node/edge/colour counts that differ across RU/EN/ZH — a change that landed in one language but not the others |
| **date** | warning | "Last updated" (box `n1100`) older than the map's last commit date |

Exit code is non-zero on any **hard** error. `--strict` also fails on drift/warnings.

The **map-vs-DSL** check imports the DSL parser from `tools/mapgen/build.py` (no Pillow, no
draw.io needed — it compares *logical content*, not pixel geometry, so it runs in CI where
draw.io isn't installed and fonts differ). It maps `English/Russian/Chinese/Spanish` →
`en/ru/zh/es.tsv`; if the source dir or a matching tsv isn't found it's skipped with a note.

Text width is measured with **Liberation Sans**, which is metric-compatible with
Arial (draw.io's default), so Latin measurement is exact. CJK uses Noto, whose
metrics only approximate draw.io's, so CJK overflow is a **warning** with a
relative margin — enough to catch gross overflows, not sub-pixel noise.

## Usage

```bash
python tools/mapcheck/check.py                 # all maps under <Lang>/Graph
python tools/mapcheck/check.py --strict         # fail on drift/warnings too
python tools/mapcheck/check.py --no-date        # skip the git-based date check
python tools/mapcheck/check.py --no-consistency # skip the map-vs-DSL check
python tools/mapcheck/check.py --maps English/Graph/roadmap.drawio.svg
```

Geometry/drift/date/map-vs-DSL checks use only the Python stdlib. box-fits-text also needs
`Pillow` and a font (Liberation Sans + Noto CJK); without them it is skipped with a
note, so the other checks still run. Install locally:

```bash
pip install Pillow      # + a Liberation Sans / Arial font on the system
```

## Known limits

- **CJK box-fits-text is approximate** (warning only) — Noto ≠ draw.io's CJK metrics.
- **drift is coarse** — it compares counts, not structure, because exact per-node y
  positions differ slightly across languages; it flags *that* drift exists (e.g. the
  ZH map still carrying duplicate edges that EN/RU dropped), not exactly where.
- **map-vs-DSL compares content, not layout** — it verifies ids, grades, and text, but not
  geometry, so a hint moved by an `angle`/`dist` edit (no text change) isn't flagged as
  stale. It also doesn't cover the chrome blocks (title/legend/About) or hint→target arrows.
- **arrows aren't validated** — nothing checks that a hint's arrow reaches its target or
  doesn't cross the tree; that still needs a rendered spot-check.
