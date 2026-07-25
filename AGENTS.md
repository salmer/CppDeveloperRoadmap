# Notes for AI agents: working on the roadmap

This file helps an AI agent (or a human) get up to speed on the repository quickly:
how the map is structured, how to edit it safely, and how to port edits between languages.

This is **not a changelog** — for what changed and when, see the git history; the owner's
current tasks live in [TODO.md](TODO.md).

> **IMPORTANT: the repository owner also edits the map by hand, in draw.io.**
> Before any edit, re-extract the XML from `<Language>/Graph/roadmap.drawio.svg` —
> do not reuse XML extracted in a previous session, or you will overwrite their changes.
> Before writing the file, check `LastWriteTime`: if it's newer than your copy, re-read it.

## Repository conventions

- **Commit messages: English only.** Article and map content is maintained in
  Russian/English/Chinese, but the git history is English.
- `main` is the primary branch; work through separate branches and pull requests.
- Article file names and URLs must not change — they are linked from outside.
- Language versions: `Russian/` is the reference (edits are made here first), then ported to
  `English/` (the root `README.md` is the English one) and `Chinese/`. There is no Spanish
  version (`Spanish/`) yet; when one appears, everything is ported to it the same way
  (see "Porting edits between languages").

## How the map is structured

- Each language's map is a single `<Language>/Graph/roadmap.drawio.svg` file: an SVG image with
  the **embedded draw.io source** in the `content` attribute of the root `<svg>` tag
  (uncompressed mxfile XML).
- **Do not hand-edit the SVG part** — only via draw.io (desktop/web/VS Code extension) or through
  the cycle "extract XML → edit XML → rebuild via the draw.io CLI".
- Color legend (fillColor): Optional `#CCEEFF`, Junior `#96BB7C`, Middle `#FAD586`,
  Senior `#BBCCEE`, pink hints `#FFD5E4`, gray stage boxes `#F5F5F5`,
  header date box `#FFF5EB`.
- External links to the map go through `goto/*.html` redirects (drawio/miro/svg) with a
  GoatCounter counter — file names and URLs must not change.

## The edit pipeline via the CLI (Windows)

1. Extract the XML from `.drawio.svg` — the `content` attribute of the root `<svg>`.
   **Only via UTF-8** (see "encoding gotcha" below).
2. Edit the XML (text edits, new `mxCell` nodes + edges). Give new nodes string ids with a
   prefix (e.g. `n900`+) so they don't collide with the numeric ones.
3. Export: `draw.io.exe -x -f svg -e -u --svg-theme auto -o out.drawio.svg in.drawio`
   (draw.io CLI, `%LOCALAPPDATA%\Programs\draw.io\`).
4. **Required**: the CLI produces a transparent background — restore it in the SVG tag:
   `style="background: #ffffff; background-color: light-dark(#ffffff, #121212); color-scheme: light dark;"`.
5. Verification: render the SVG in **headless Edge**
   (`msedge --headless=new --screenshot=... --window-size=...` plus an HTML wrapper with
   panes over the regions of interest) and run a bbox overlap check (0 overlaps is mandatory).
   Do not trust the interactive browser render or the PNG export on this large SVG.

> **Encoding gotcha (important!):** the XML must be extracted via UTF-8:
> `[IO.File]::ReadAllText($svg, [Text.Encoding]::UTF8)` + `LoadXml`, NOT `Get-Content -Raw`
> (PowerShell 5 reads it with the system codepage and mangles Chinese into double mojibake).
> Save with a `StreamWriter` using `UTF8Encoding($false)` (no BOM). The English map is pure
> ASCII and is unaffected; the Chinese map is affected.

## Map layout rules

- **Update the date in the header on every map edit.** The header has a box
  "Last updated: DD.MM.YYYY" (id `n1100`). The box deliberately has a light fill
  `#FFF5EB` (not bare text): black text on a bare background is invisible in dark theme, because
  the SVG uses a `light-dark()` background. Same rule for any new labels — a bare
  `fontColor=#000000` without a light box is unreadable on a dark background.
- **Stage-frame title band ~37px.** For the "Stage N" frames (id 2–11) the top margin down to the
  first node is ~37px (exception — frame 2, where it's 61px); the label sits in this band
  (`verticalAlign=top`). Hence the limit on label font size: **~28px max** fits without shifting
  nodes. For emphasis use `fontStyle=1` (bold) rather than a larger size — that doesn't change
  the height.
- **Stage frames are ordinary vertices, not containers** (`container=0`, children are not nested).
  If you shift content vertically, the frame has to be grown separately, otherwise nodes spill
  out. After any shift, check for each frame: frame bottom ≥ bottom of the lowest element inside it.
- **Edge attachment points.** A legacy of the Miro import — some edges have arbitrary
  `exitX/exitY`, `entryX/entryY`, so they leave one side of a node in a fan from different points.
  Normalization: attach to the middle of the side facing the line (determine the side from the
  first waypoint for the exit / the last for the entry); if the reference point is inside the
  node's bbox, leave it alone (this preserves intentional downward exits); skip edges with the
  `curved=1` style (hint callouts) entirely.
- **Known layout gotchas:**
  - edges have explicit waypoint arrays (`<Array as="points">`) and vertical "buses"
    (trunk lines at a fixed x); build new edges to the same pattern, routing horizontal segments
    in the empty bands between rows of boxes (row pitch 60px, box height 30px);
  - if you move a node explicitly and then run a general shift rule, the node moves **twice**;
    exclude such nodes from the general pass or shift them after it;
  - line breaks in node text are `&#xa;` in the `value` attribute.

## Porting edits between languages

Edits are made in the Russian map first, then ported to the English and Chinese ones.

- **The vertical structure of the maps is identical across languages** — the stage frames and all
  rows share y-coordinates. Only x/width differ (translation changes node widths). So vertical
  shifts port one-to-one along the same y-thresholds.
- **gate and hub-x are language-dependent** (the map center is at a different x): only the right
  (hard skills) half shifts, `x ≥ gate`; section headers ("C++ syntax", "OS", …) sit left of the
  gate and don't shift. The "elbows" of the central trunk (at the level of the "Hard skills" node)
  must not move during vertical shifts, or the map's central line breaks.
  Current-state reference points: RU gate=2900 hub-x=2945.25; EN gate=3000 hub-x=3044.52;
  ZH gate=2900 hub-x=2680.04.
- **Node ids in the upper part of the map (syntax, templates, libraries) are shared across
  languages**, but they diverge lower down. Known RU→EN/ZH divergences: `242→241` (Dev practices),
  `275→274` (Profilers), `277→276` (Industrial standards), `341→340` (Multithreading),
  `379→378` (Security). Find a new node's parent by this map, not blindly by id.
- New nodes are copied whole from the Russian map and translated rigidly by
  `delta = parent_position(target) − parent_position(RU)`; the text comes from the translation,
  the width is fit to the translation; edges reuse the same waypoints + delta; remap the
  `source/target` of divergent ids. Then normalize the attachment points.
- **Chinese nodes are wider** (the "中文（English）" format), so individual columns may need to
  be shifted right so they don't overlap their neighbors; verify with the overlap check.

## Open questions

- **The fate of Miro.** The Miro boards (external) don't sync with draw.io and have fallen behind;
  they are marked obsolete in the README of every language. Optional plan: check GoatCounter
  traffic for `/goto/miro-*` vs `/goto/svg-*`; if traffic is low, put a "the map has moved" banner
  on the boards and redirect `goto/miro` to the SVG viewer (without breaking links).
- **The owner's current tasks are in [TODO.md](TODO.md)**; no need to duplicate them here,
  check it directly.
