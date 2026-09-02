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
   - 文字（标签、提示、日期）→ `en.tsv` / `ru.tsv` / `zh.tsv` / `es.tsv` 中对应的行（新节点需要在**四个文件中都**加一行）。
2. **仅首次需要** — 准备好你的环境：
   ```bash
   python tools/mapgen/setup.py --venv
   ```
   它会创建虚拟环境、安装 Pillow，并检查两个它无法替你安装的东西（CJK 字体和 draw.io
   桌面应用），如果缺少就打印适用于你操作系统的确切命令。
3. 在仓库根目录用一条命令重新构建、更新全部四张地图并进行校验：
   ```bash
   python tools/mapgen/build.py --dir tools/mapgen/roadmap --deploy --check
   ```
   `--deploy` 会把每张构建好的地图复制到对应的 `<Language>/Graph/roadmap.drawio.svg`，
   `--check` 随后运行 `mapcheck`。构建前依赖会再次被检查：如果缺少依赖（或者忘记激活虚拟
   环境），该命令会立刻告诉你。
4. 创建一个包含源文件**和**重新生成的地图的 pull request。

DSL 语法和细节见 [`tools/mapgen/README.md`](../../tools/mapgen/README.md)。无法运行构建？
仍然编辑源文件并在 PR 中说明——维护者会重新生成地图。
