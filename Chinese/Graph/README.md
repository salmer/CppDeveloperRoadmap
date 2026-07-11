# 如何查看和编辑路线图

路线图存储在 [roadmap.drawio.svg](roadmap.drawio.svg) 文件中——这是一个普通的 SVG 图像，其中嵌入了可编辑的 [draw.io](https://www.drawio.com) 图表。同一个文件既是您看到的图片，也是您编辑的源文件，因此无需导出或保持同步：每个被接受的 pull request 都会立即更新发布的路线图。

## 查看

- 在网站上：[salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=zh](https://salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=zh)
- 在 GitHub 上：打开 [roadmap.drawio.svg](roadmap.drawio.svg)——它会以图像形式呈现。

## 编辑

1. Fork 本仓库。
2. 在 draw.io 编辑器中打开图表：
   - **网页版：** 访问 [sketch.diagrams.net](https://sketch.diagrams.net)（draw.io 的白板风格界面），从 *GitHub* 打开文件，授权后在您的 fork 中选择 `Chinese/Graph/roadmap.drawio.svg`。保存时会直接提交到您的 fork。
   - **VS Code：** 安装 [Draw.io Integration 扩展](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio)后打开该文件（也可以通过 github.dev 在浏览器中使用——在您的 fork 页面按 `.` 键）。
   - **桌面版：** [draw.io 桌面应用](https://www.drawio.com)。
3. 创建包含您更改的 pull request。

> :warning: 请勿在 draw.io 之外手动编辑 SVG 文本——这可能会删除嵌入的图表源，使文件无法再编辑。文件开头的注释也有同样的警告。
