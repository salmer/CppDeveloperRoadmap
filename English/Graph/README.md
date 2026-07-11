# How to view and edit the roadmap

The roadmap is stored as [roadmap.drawio.svg](roadmap.drawio.svg) — a regular SVG image with the editable [draw.io](https://www.drawio.com) diagram embedded inside it. The same file is both the picture you see and the source you edit, so there is nothing to export or keep in sync: every accepted pull request updates the published roadmap immediately.

## Viewing

- On the site: [salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=en](https://salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=en)
- On GitHub: open [roadmap.drawio.svg](roadmap.drawio.svg) — it renders as an image.

## Editing

1. Fork the repository.
2. Open the diagram in one of the draw.io editors:
   - **Web:** go to [sketch.diagrams.net](https://sketch.diagrams.net) (the whiteboard-style UI of draw.io), open the file from *GitHub*, authorize, and select `English/Graph/roadmap.drawio.svg` in your fork. Saving commits directly to your fork.
   - **VS Code:** install the [Draw.io Integration extension](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) and open the file (this also works in the browser via github.dev — press `.` on your fork).
   - **Desktop:** the [draw.io desktop app](https://www.drawio.com).
3. Open a pull request with your change.

> :warning: Do not edit the SVG text by hand outside draw.io — that can strip the embedded diagram source and make the file uneditable. The file starts with a comment saying the same.
