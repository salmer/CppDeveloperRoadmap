# :package: 流行的库与框架

C++ 没有像 JavaScript 的 npm 或 Rust 的 crates.io 那样统一的"标准"生态，所以所用的库很大程度上取决于领域。即便如此，还是有几个名字在招聘启事和项目中出现得比其他的更频繁——下面收录的正是这些。

不要试图一次学完所有东西。把自己领域里的一两个库真正学扎实，远比浮于表面地知道十来个更有用。把它们引入项目最简单的方式是通过 Conan 或 vcpkg 包管理器——见[语言工具包](Tooling.md)。

> :compass: 这是一篇概览性的文章和一个导航起点，而不是一份完整的目录。实际存在的库要多出好几个数量级，针对具体任务几乎总能再找到别的东西——请在你自己的问题领域里搜索、看看类似项目用了什么、并对照较新的清单（例如 [awesome-cpp](https://github.com/fffaraz/awesome-cpp)）。这份清单的目的，是给刚起步的人一个立足点。

> :bulb: 开发工具（编译器、调试器、分析器、测试框架）单独放在另一篇文章里——[语言工具包](Tooling.md)。

## :hammer_and_wrench: 通用

* :arrow_forward: **Boost** - [boost.org](https://www.boost.org)

    一个庞大的库集合，历史上一直充当标准库的"试验场"：今天标准中的许多东西（智能指针、`filesystem`、`optional`、`variant`）都是先在 Boost 里打磨的。它现在依然有用——里面有一些标准至今仍然缺失的东西。另一面是体积：为了一个功能而引入整个 Boost 是不明智的，它的大多数库都可以单独取用。

* :arrow_forward: **{fmt}** - [github.com/fmtlib/fmt](https://github.com/fmtlib/fmt)

    一个字符串格式化库，成了 C++20 中 `std::format` 的基础。比 `printf` 更快更安全，比 `iostream` 流更易读。如果你的编译器还不支持 `std::format`，或者你需要超出标准的能力，用它就有意义。

* :arrow_forward: **spdlog** - [github.com/gabime/spdlog](https://github.com/gabime/spdlog)

    一个建立在 {fmt} 之上的快速日志库。它支持输出到带轮转的文件、带高亮的控制台，以及异步模式。在无法接入调试器的生产环境中，日志是主要的诊断手段之一。

* :arrow_forward: **range-v3** - [github.com/ericniebler/range-v3](https://github.com/ericniebler/range-v3)

    C++20 中 `std::ranges` 所基于的参考实现。它让你能够以链式的方式编写序列变换，不需要显式的迭代器和临时容器。如果你需要尚未进入标准的特性、或者需要支持较旧的编译器，它就很有用。

## :globe_with_meridians: 网络与数据交换

* :arrow_forward: **Asio** - [think-async.com/Asio](https://think-async.com/Asio/)

    C++ 中异步 I/O 事实上的标准，也是许多网络项目的基础。它有两种形态：作为独立库，以及作为 Boost 的一部分。它与 C++20 协程配合得很好。正是以它为基础，人们多次提议把一个网络库纳入标准。

* :arrow_forward: **nlohmann/json** - [github.com/nlohmann/json](https://github.com/nlohmann/json)

    C++ 中最流行的 JSON 处理库。它受到青睐的原因是：用它写出来的代码几乎像一门内置支持 JSON 的语言。只需引入一个头文件即可。如果解析大数据量的速度很关键，值得看看更快的替代品，比如 simdjson 或 RapidJSON。

* :arrow_forward: **Protocol Buffers** - [protobuf.dev](https://protobuf.dev)

    来自 Google 的一种带 schema 的二进制序列化格式：数据结构在一个单独的文件里描述，并由它生成代码。比 JSON 更紧凑、更快，而 schema 又提供了版本兼容性的控制——当客户端和服务器不同时更新时，这是一个重要的特性。

* :arrow_forward: **gRPC** - [grpc.io](https://grpc.io)

    一个建立在 Protocol Buffers 和 HTTP/2 之上的远程过程调用框架。它在微服务架构中很常见，包括服务用不同语言编写的那种组合。

* :arrow_forward: **POCO** - [pocoproject.org](https://pocoproject.org)

    一套用于网络和服务器应用的跨平台库：HTTP 客户端和服务器、数据库访问、XML 和 JSON 解析、日志。就风格而言，它更接近"自带电池"，而不是一组各司其职的小库。

## :framed_picture: 图形用户界面

* :arrow_forward: **Qt** - [qt.io](https://www.qt.io)

    C++ 中最广泛使用的桌面应用框架，早已超出了 GUI 的范畴：它包含网络、数据库、线程、格式解析。它是跨平台的，有自己的 IDE（Qt Creator）。一个重要的细节是许可：开放版本以 LGPL/GPL 分发，而封闭的商业产品可能需要付费许可。这些条款值得在开始开发**之前**就研究清楚。

## :bar_chart: 计算、图形与机器学习

* :arrow_forward: **OpenCV** - [opencv.org](https://opencv.org)

    计算机视觉中事实上的标准：图像和视频处理、目标检测、相机标定。它被用在机器人、工业质量检测、医学影像中。

* :arrow_forward: **Eigen** - [libeigen.gitlab.io](https://libeigen.gitlab.io/)

    一个线性代数库：矩阵、向量、求解方程组。它仅由头文件组成，并做了激进的优化。它常出现在机器人、仿真和计算机视觉中。

* :arrow_forward: **CUDA** - [developer.nvidia.com/cuda-toolkit](https://developer.nvidia.com/cuda-toolkit) 和 **OpenCL** - [khronos.org/opencl](https://www.khronos.org/opencl/)

    在显卡上做计算的两种途径。CUDA 只能在 NVIDIA 硬件上运行，但更成熟、更好用；OpenCL 是一个开放标准，可以在不同厂商的硬件上运行。在任务能很好并行化的地方它们很受欢迎：科学计算、图像处理、机器学习。

* :arrow_forward: **LibTorch (PyTorch C++)** - [pytorch.org/cppdocs](https://pytorch.org/cppdocs/) 和 **TensorFlow** - [tensorflow.org](https://www.tensorflow.org)

    两大主流机器学习框架的 C++ API。模型训练通常在 Python 里进行，而 C++ 用在部署阶段：当一个训练好的模型需要在有严格速度要求、或者不能依赖 Python 的应用程序内部运行时。

## :link: 与其他语言的互操作

* :arrow_forward: **pybind11** - [github.com/pybind/pybind11](https://github.com/pybind/pybind11)

    它让你能把 C++ 代码做成一个可被 Python 导入的模块。典型的场景是：繁重的计算用 C++ 写，而上层逻辑和实验留在 Python 里。许多知名项目的封装层都建立在 pybind11 之上。

---

[**回到主页**](README.md)
