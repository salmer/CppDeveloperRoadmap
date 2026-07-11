# Contributing to C++ Developer Roadmap

Thank you for your interest in contributing! To maintain consistency and quality across the roadmap, please adhere to the following guidelines.

## Language Sync Rule

This project maintains parity across three languages: English (`English/`), Russian (`Russian/`), and Chinese (`Chinese/`).
**Any content change (e.g., adding a book, updating a tool, fixing a description) MUST be mirrored across all three languages.** 
If you are unable to translate the content into all languages, please create an issue or note it in your Pull Request so someone can help translate it.

## Editing the Roadmap

The roadmap is one `roadmap.drawio.svg` file per language (`English/Graph/`, `Russian/Graph/`, `Chinese/Graph/`) — an SVG image with the editable draw.io diagram embedded inside it. Edit it only with a draw.io editor (sketch.diagrams.net — the whiteboard-style UI with GitHub integration, the draw.io desktop app, or the VS Code extension) and submit the change as a normal pull request; see the per-language `Graph/README.md` for step-by-step instructions. **Never edit the SVG text by hand** — that can strip the embedded source and make the file uneditable. The language sync rule applies to the roadmap too: structural changes should be mirrored in all three language files.

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

### Local Link Checking

Before opening a PR, please run `lychee` locally to verify links. Run the following command (requires `lychee` to be installed):

```bash
lychee --no-progress --accept "200..=204,429" --max-retries 2 --timeout 45 "**/*.md"
```
This command must exit with code 0. Run this after ANY link change.
