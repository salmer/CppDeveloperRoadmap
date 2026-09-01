## Description
Please include a summary of the change and which issue is fixed.

## Checklist
- [ ] Content changes have been applied to all three languages (English, Russian, Chinese) OR a follow-up issue has been opened to track missing translations.
- [ ] Any new external links have been verified. (If a link is bot-blocked and fails CI, it has been added to `.lycheeignore` with a comment).
- [ ] I have run `lychee --offline --no-progress "**/*.md"` locally (see `CONTRIBUTING.md`); if I added external links, I checked those too.
- [ ] **If I changed the map**: I edited `tools/mapgen/roadmap/` (not the `.drawio.svg`), rebuilt with `python tools/mapgen/build.py --dir tools/mapgen/roadmap --deploy --check`, and committed the regenerated maps — or I said in the description that a maintainer needs to regenerate them.
