# Contributing to C++ Developer Roadmap

Thank you for your interest in contributing! To maintain consistency and quality across the roadmap, please adhere to the following guidelines.

## Language Sync Rule

This project maintains parity across three languages: English (`English/`), Russian (`Russian/`), and Chinese (`Chinese/`).
**Any content change (e.g., adding a book, updating a tool, fixing a description) MUST be mirrored across all three languages.** 
If you are unable to translate the content into all languages, please create an issue or note it in your Pull Request so someone can help translate it.

This rule is about the **articles** (the `.md` files). **The map is different** — it has one shared source, so a structural change is made once and regenerated into all three languages; only its *text* is per-language. See below.

## Editing the Roadmap

The roadmap is **generated** from a single language-neutral source in [`tools/mapgen/roadmap/`](tools/mapgen/roadmap) — `structure.dsl` (topology, grades, stages, layout) plus one `<lang>.tsv` per language (just the text). `build.py` renders it to the three `<Language>/Graph/roadmap.drawio.svg` files.

**Do not hand-edit the `.drawio.svg` maps** — they are build output, and CI (`mapcheck`) fails if a committed map no longer matches the source. To change the map:

1. Edit `structure.dsl` (to add/move/re-grade a node or a hint) and/or the `<lang>.tsv` files (to change text — one row per language).
2. Set your machine up once — `python tools/mapgen/setup.py --venv` creates a virtualenv, installs Pillow, and tells you how to install the draw.io desktop app if you don't have it.
3. Rebuild and update all three maps with one command from the repo root, then open a pull request:
   ```bash
   python tools/mapgen/build.py --dir tools/mapgen/roadmap --deploy --check
   ```
   See [`tools/mapgen/README.md`](tools/mapgen/README.md) for the DSL grammar and all flags.

Because there is one structural source, a structural change lands in all three languages at once — you only supply the per-language **text** in each `<lang>.tsv`. If you can't run the build locally (`setup.py` will tell you what's missing — the draw.io desktop app is the usual blocker), edit the source anyway and say so in your PR; a maintainer will regenerate the maps. To just *view* the map, see the per-language [`Graph/README.md`](English/Graph/README.md).

## Local Jekyll Preview

To preview the site locally using GitHub Pages:
1. Ensure you have Ruby and Bundler installed.
2. Install dependencies: `bundle install`
3. Serve the site: `bundle exec jekyll serve`
4. Open the provided localhost URL in your browser.

## Link Policy

We use `lychee` to ensure all links are valid.

* **.lycheeignore**: Some valid domains (like Amazon, Reddit, or CppReference) block bots or CI IPs, resulting in false positives (403 or redirect loops). These are added to `.lycheeignore`.
* **Dead Links**: If you find a dead link, please replace it with a Wayback Machine snapshot. Note it as an "(archived copy)" in the file's respective language.
* **Manual Sweep**: Since Amazon links and other bot-blocking domains are in `.lycheeignore`, they are invisible to CI. A periodic manual sweep is required to ensure these links remain active.

### How links are checked in CI

Two separate workflows, so a third-party outage can never block your PR:

| | when | scope | on failure |
|---|---|---|---|
| **Check links** | every PR | **internal** links only (relative paths between files) | fails the PR — these are real breakages you introduced |
| **Link audit** | 1st of each month, or on demand | **all external** URLs | files/updates a "Link Checker Report" issue; blocks nothing |

### Local Link Checking

Before opening a PR, run the same internal check CI runs — it takes milliseconds and needs no network:

```bash
lychee --offline --no-progress "**/*.md"
```

If you added or changed an **external** link, check that too (this one hits the network, so an occasional failure may just be the far end being slow):

```bash
lychee --no-progress --accept "200..=204,429" --max-retries 2 --timeout 45 "**/*.md"
```

Both must exit 0. If an external site is alive in your browser but fails from CI (403/415, or a redirect loop — common for sites that block datacenter IPs), add it to `.lycheeignore` with a comment explaining why.
