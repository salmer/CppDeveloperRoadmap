# 如何查看和编辑路线图

[roadmap.drawio.svg](roadmap.drawio.svg) 是一个普通的 SVG 图像，内嵌了 [draw.io](https://www.drawio.com)
图表——在任何地方打开都能看到路线图。但它是**自动生成的**：真正的源文件是
[`tools/mapgen/roadmap/`](../../tools/mapgen/roadmap) 中与语言无关的文本描述，因此这个 `.drawio.svg`
只是构建产物，而不是你要编辑的对象。

## 查看

- 在网站上：[salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=zh](https://salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=zh)
- 在 GitHub 上：打开 [roadmap.drawio.svg](roadmap.drawio.svg)——它会以图像形式呈现。
- 交互式查看：[draw.io 查看器](https://salmer.github.io/CppDeveloperRoadmap/goto/drawio/?l=zh)（仅查看——在那里的改动不会被保存）。

## 编辑

路线图由 `tools/mapgen/roadmap/` 生成——`structure.dsl`（节点树、等级、阶段、提示框）和每种语言一个
`<lang>.tsv`（仅文本）。**请勿手动编辑此 `.drawio.svg`**——它会从源文件重新生成，且 CI（`mapcheck`）
会拒绝与源文件不一致的地图。

1. Fork 本仓库并编辑源文件：
   - 节点、其等级/阶段或提示 → `tools/mapgen/roadmap/structure.dsl`
   - 文字（标签、提示、日期）→ `en.tsv` / `ru.tsv` / `zh.tsv` 中对应的行（新节点需要在**三个文件中都**加一行）。
2. 重新构建并复制地图（需要 Python + Pillow + draw.io 桌面版 CLI）：
   ```bash
   pip install -r tools/mapgen/requirements.txt
   python tools/mapgen/build.py --dir tools/mapgen/roadmap --langs en,ru,zh
   cp tools/mapgen/roadmap/en.drawio.svg English/Graph/roadmap.drawio.svg
   cp tools/mapgen/roadmap/ru.drawio.svg Russian/Graph/roadmap.drawio.svg
   cp tools/mapgen/roadmap/zh.drawio.svg Chinese/Graph/roadmap.drawio.svg
   ```
3. 检查：`python tools/mapcheck/check.py --no-date`（0 个硬错误），然后创建一个包含源文件**和**重新生成的地图的 pull request。

DSL 语法和细节见 [`tools/mapgen/README.md`](../../tools/mapgen/README.md)。无法运行构建？
仍然编辑源文件并在 PR 中说明——维护者会重新生成地图。
