# How to view and edit the roadmap

[roadmap.drawio.svg](roadmap.drawio.svg) is a regular SVG image with a [draw.io](https://www.drawio.com)
diagram embedded inside it — open it anywhere to see the map. It is **generated**: the real
source is a language-neutral text description in [`tools/mapgen/roadmap/`](../../tools/mapgen/roadmap),
so this `.drawio.svg` is build output, not the thing you edit.

## Viewing

- On the site: [salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=en](https://salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=en)
- On GitHub: open [roadmap.drawio.svg](roadmap.drawio.svg) — it renders as an image.
- Interactively: the [draw.io viewer](https://salmer.github.io/CppDeveloperRoadmap/goto/drawio/?l=en) (view only — changes there are not saved back).

## Editing

The map is built from `tools/mapgen/roadmap/` — `structure.dsl` (the node tree, grades,
stages, hint boxes) and one `<lang>.tsv` per language (just the text). **Do not edit this
`.drawio.svg` by hand** — it is regenerated from the source, and CI (`mapcheck`) rejects a map
that has drifted from it.

1. Fork the repository and edit the source:
   - a node, its grade/stage, or a hint → `tools/mapgen/roadmap/structure.dsl`
   - wording (a label, a hint, the date) → the matching row in `en.tsv` / `ru.tsv` / `zh.tsv`
     (a new node needs a row in **all three**).
2. Rebuild and copy over the maps (needs Python + Pillow + the draw.io desktop CLI):
   ```bash
   pip install -r tools/mapgen/requirements.txt
   python tools/mapgen/build.py --dir tools/mapgen/roadmap --langs en,ru,zh
   cp tools/mapgen/roadmap/en.drawio.svg English/Graph/roadmap.drawio.svg
   cp tools/mapgen/roadmap/ru.drawio.svg Russian/Graph/roadmap.drawio.svg
   cp tools/mapgen/roadmap/zh.drawio.svg Chinese/Graph/roadmap.drawio.svg
   ```
3. Check it: `python tools/mapcheck/check.py --no-date` (0 hard errors), then open a pull
   request with the source **and** the regenerated maps.

See [`tools/mapgen/README.md`](../../tools/mapgen/README.md) for the DSL grammar and details.
Can't run the build? Edit the source anyway and note it in your PR — a maintainer will
regenerate the maps.
