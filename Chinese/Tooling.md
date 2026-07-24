# :triangular_ruler: 语言工具包

新手开发者通常对于可用的工具了解有限，这些工具可以使编写代码更加容易、提高效率并防止许多错误。这些工具不是解决语言可能出现的困难的万能药，但它们可以化腐朽为神奇。以下是全球开发人员公认的常见和流行的工具列表，但这只是其中一小部分。随着时间推移，您将会更加熟悉这些工具，并发现适合自己需求的新工具。

## :gear: 编译器

* :arrow_forward: **GCC (GNU Compiler Collection)**

    网址：https://gcc.gnu.org  
    价格：免费

    大多数 Linux 发行版的默认编译器，也是世界上使用最广泛的 C++ 编译器之一。它紧跟最新的语言标准，并能生成高度优化的代码。在 Windows 上可以通过 MSYS2 和 MinGW-w64 项目使用。

* :arrow_forward: **Clang**

    网址：https://clang.llvm.org  
    价格：免费

    基于 LLVM 基础设施构建的编译器，也是 macOS 上的默认编译器。它以编译速度快、错误信息清晰友好著称，非常适合初学者。Clang 还是一整套开发者工具的基础，例如 clang-format、clang-tidy 以及许多编辑器使用的 clangd 语言服务器。

* :arrow_forward: **MSVC (Microsoft Visual C++)**

    网址：https://visualstudio.microsoft.com  
    价格：包含在 Visual Studio 中（社区版免费）

    微软的编译器，随 Visual Studio 一起发布，是 Windows 开发的首选。大多数 Windows 商业软件和游戏项目都使用它构建。

    **提示：** 使用 [Compiler Explorer](https://godbolt.org)，无需安装任何东西，即可在三种编译器上并排快速测试您的代码。

## :page_facing_up: 文本编辑器

* :arrow_forward: **Visual Studio Code**

    网址：https://code.visualstudio.com/  
    价格：免费  

    提供强大而高效的文本文件和源代码编辑器。它拥有丰富的扩展库，可根据个人喜好进行定制化设置。还可以配置为与源代码一起使用，轻松编译、运行和调试您的代码。此外，它还拥有一个强大搜索引擎来查找文件和文件夹，在处理大型项目时更容易搜索、阅读和操作。

* :arrow_forward: **Notepad++**

    网址：https://notepad-plus-plus.org/  
    价格：免费

    轻量级文本文件和源代码编辑器。支持常见编程语言语法高亮显示功能。相比于 Visual Studio Code，它更方便快速打开和查看文件，并且由于其轻量级设计，在处理大量文本文件时非常舒适。

## :open_file_folder: IDE（集成开发环境）

* :arrow_forward: **Microsoft Visual Studio IDE**

    网址：https://visualstudio.microsoft.com  
    价格：社区版免费

    来自 Microsoft 的集成开发环境（IDE），提供了一套全面的工具，包含各种程序设计语言以及跨平台开发所需要用到得编码器、编译器、调试器以及分析仪等等。对初学者来说是一个很好选择，因为其拥有友好的界面，并且初始状态下不需要进行过多的自定义设置。

* :arrow_forward: **Qt Creator IDE**

     网址：https://www.qt.io/product/development-tools  
     价格：开放源码项目免费（详细信息请参考 [Qt Open Source](https://www.qt.io/download-open-source?hsCtaTracking=9f6a2170-a938-42df-a8e2-a9f0b1d6cdce%7C6cb0de4f-9bb5-4778-ab02-bfb62735f3e5)）

    最初 Qt Creator 是作为 C++ 应用程序图形界面开发 IDE 而定位。随着时间推移，框架已经拥有了众多功能并演变成跨平台应用程序的综合生态系统。它提供了广泛基础库原件以满足各种需求，如网络连接，图形接口，数据库操作和处理像图片或文本格式之类流行格式。如今 Qt Creator 成为 Visual Studio 的竞争对手，并特别受到创建适用于各种 Linux 发行版应用程序的开发人员的欢迎。

* :arrow_forward: **Xcode**

    网址：https://developer.apple.com/xcode/  
    价格：免费

    Apple 自家的开发环境，也是为 macOS 和 iOS 构建应用程序的唯一途径。它随附 Clang 和 LLDB。如果你在 macOS 上工作，即使你更喜欢用别的编辑器写代码，至少也会为了它的命令行工具而需要 Xcode。

* :arrow_forward: **JetBrains CLion IDE**  
     CLion 是来自 JetBrains 公司的强大跨平台 IDE。与其他 IDE 一样，它提供了全面的工具集，方便软件开发，并且非常适合 C 和 C++中进行跨平台开发。自 2025 年 5 月起，CLion 对非商业用途免费；商业开发需要付费许可证。

## :flashlight: 扩展

* :arrow_forward: **JetBrains ReSharper C++**  
   JetBrains ReSharper C++ 是 Microsoft Visual Studio 的扩展程序之一，它增加了高级源代码处理功能，如扩展代码突出显示和提示、构建项目间依赖关系图、纠正常见错误推荐、调试期间改进信息、改进搜索并导航到项目等等，可与 Visual Assist 竞争。

* :arrow_forward: **Visual Assist**  

    网址：https://www.wholetomato.com  

    一个为微软 Visual Studio 提供额外功能的扩展，如增强代码高亮和提示、调试和编码期间增加信息、高级搜索能力以及改进的项目导航。它与 JetBrains ReSharper 竞争。

* :arrow_forward: **Incredibuild**  

    网址：https://www.incredibuild.com

    这是一个用于分布式编译项目的应用程序/扩展，它将所有开发者工作站合并成一个单一的网络，提供使用数十台机器来组装和编译源代码的可能性。这可以加速大型项目的构建过程。

## :electric_plug: 包管理器和构建系统

* :arrow_forward: **CMake**

    网址：https://cmake.org  
    价格：免费

    一个跨平台的自动化系统，用于从源代码构建应用程序，并生成必要的工件以便在目标平台上进行后续组装。它目前被认为是从源码构建各种库时的标准工具。

* :arrow_forward: **Conan**

    网址：https://conan.io  
    价格：免费

    一个用于组织 C++ 库和框架的软件包管理器和依赖项管理器。它支持在 Windows 和 Linux 等各种平台上工作，并与 CMake 和 Visual Studio 等工具集成。

* :arrow_forward: **vcpkg**

    网址：https://vcpkg.io  
    价格：免费

    由微软开发的免费开源 C/C++ 库包管理器。它提供数千个即用型库，并与 CMake 和 Visual Studio 无缝集成。与 Conan 一起，它是 C++ 生态系统中最流行的两个依赖管理器之一。

* :arrow_forward: **Ninja**

    网址：https://ninja-build.org  
    价格：免费

    PC 和 C++应用程序的项目构建管理器。该管理器的主要优点是快速项目组装。它支持跨平台开发，并与所有流行的编译器兼容。

* :arrow_forward: **ccache**

    网址：https://ccache.dev  
    价格：免费

    编译器缓存：它会存储以前的编译结果，并在再次进行相同的编译时重用它们，这可以极大地加快重新构建的速度。它透明地位于 GCC 或 Clang 之前，并只需几行代码即可与 CMake 集成，使其成为中大型项目中在构建时间方面最廉价的收益之一。

## :mag: 代码分析器和格式化工具

* :arrow_forward: **clang-format**

    网址：https://clang.llvm.org/docs/ClangFormat.html  
    价格：免费

    C++ 事实上的标准自动代码格式化工具。在仓库中存放一个配置文件（`.clang-format`）即可保持整个团队代码风格的一致性，并消除代码审查中关于格式的争论。几乎所有编辑器和 IDE 都开箱即用地支持它。

* :arrow_forward: **clang-tidy**

    网址：https://clang.llvm.org/extra/clang-tidy/  
    价格：免费

    来自 LLVM 项目的静态分析工具（linter）。它根据数百条规则检查代码——易出错的模式、性能问题、可读性、现代 C++ 风格——并能自动修复它发现的许多问题。它已集成到大多数 IDE 中，包括 Visual Studio、CLion、VS Code 和 Qt Creator。

* :arrow_forward: **Sanitizers（ASan、UBSan、TSan）**

    网址：https://github.com/google/sanitizers  
    价格：免费

    直接内置于 GCC、Clang 和 MSVC 中的动态分析工具，通过编译器标志启用（例如 `-fsanitize=address`）。AddressSanitizer 捕获内存错误（如越界访问和 use-after-free），UndefinedBehaviorSanitizer 捕获未定义行为，ThreadSanitizer 捕获数据竞争。在启用 sanitizers 的情况下运行测试被认为是现代 C++ 开发的基本实践。

* :arrow_forward: **模糊测试（libFuzzer、AFL++）**

    网址：https://llvm.org/docs/LibFuzzer.html, https://github.com/AFLplusplus/AFLplusplus  
    价格：免费

    模糊测试就是自动向代码喂入一连串随机的、故意畸形的数据，以寻找崩溃和挂起。它对任何解析外部输入的东西尤其有用：格式解析器、网络协议、解码器。它通常与 sanitizers 一起运行——模糊器找到触发错误的输入，而 sanitizer 指出错误究竟发生在哪里。libFuzzer 内置于 Clang，AFL++ 则作为独立工具运行。

* :arrow_forward: **PVS Studio**

    网址：https://pvs-studio.com  
    价格：付费；开源项目和学生免费

    由 PVS-Studio 开发的跨平台（Windows、Linux、MacOS）静态代码分析器。该分析器的主要目标是对源代码进行分析，以检测编译器或代码审查期间可能未被发现的各种错误。它有助于减少与语言语法和陷阱相关的错误数量。

* :arrow_forward: **Cppcheck**

    网址：https://cppcheck.sourceforge.io  
    价格：免费

    一个免费的代码分析器，可以帮助您捕捉编译器或代码审查期间可能被忽略的源代码中常见错误。它是跨平台的，并支持流行的 Linux 发行版和 Windows。

* :arrow_forward: **Valgrind**

    网址：https://valgrind.org  
    价格：免费

    一组工具，可以帮助您在应用程序运行时调查各种问题，例如内存泄漏和性能分析。它与多个 Linux 发行版兼容。在现代项目中，sanitizers 以更低的开销覆盖了许多相同的使用场景，但 Valgrind 无需重新编译，因此仍然很有用。

## :beetle: 调试器

* :arrow_forward: **GDB (GNU Debugger)**

    网址：https://sourceware.org/gdb/  
    价格：免费

    GNU/Linux 世界中的标准调试器。它允许您设置断点、单步执行代码、检查变量和内存，以及分析崩溃应用程序的核心转储（core dump）。Linux 上大多数 IDE 的调试前端（VS Code、Qt Creator、CLion）底层都使用 GDB，因此即使您主要在 IDE 中调试，了解它的基础知识也很有价值。

* :arrow_forward: **LLDB**

    网址：https://lldb.llvm.org  
    价格：免费

    来自 LLVM 项目的调试器，也是 macOS 上的默认调试器（Xcode 使用它）。它提供与 GDB 类似的功能，但架构更现代。

* :arrow_forward: **WinDbg**

    网址：https://learn.microsoft.com/windows-hardware/drivers/debugger/  
    价格：免费

    微软面向 Windows 的调试器。在 Windows 上的日常工作中，通常内置于 Visual Studio 的调试器就够用了，但在它力所不及的地方，WinDbg 不可或缺：分析来自生产机器的崩溃转储、调试驱动和内核模式、处理没有源码的应用程序。对于从事底层开发、或排查用户机器上崩溃的人来说，这是一项有用的技能。

## :stopwatch: 性能分析器

* :arrow_forward: **perf**

    网址：https://perfwiki.github.io/main/  
    价格：免费

    Linux 上的标准采样性能分析器，内置于内核中。它能显示应用程序实际消耗 CPU 时间的位置，并在需要时提供硬件计数器细节（如缓存未命中、分支预测错误）。通常与火焰图 (flame-graph) 可视化一起使用，使性能瓶颈一目了然。

* :arrow_forward: **Tracy**

    网址：https://github.com/wolfpld/tracy  
    价格：免费

    一种实时帧性能分析器，在游戏开发中尤为流行。你可以使用轻量级宏在代码中标记区域，并在图形客户端中实时观察计时，精确到各个帧和线程。它跨平台且开销极低。

* :arrow_forward: **Intel VTune Profiler**

    网址：https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html  
    价格：免费

    一款功能强大的性能分析器，用于 x86 架构上的深度性能分析：瓶颈、线程效率、内存访问模式以及微架构级别的指标。当 `perf` 输出不够详细时的首选工具。在 Windows 上，Visual Studio IDE 也内置了功能强大的 CPU 和内存性能分析器。

## :white_check_mark: 测试与基准测试

* :arrow_forward: **GoogleTest (gtest/gmock)**

    网址：https://github.com/google/googletest  
    价格：免费

    C++ 中使用最广泛的单元测试框架。它附带 GoogleMock 用于创建桩和 mock，从而让你能把代码与它的依赖——数据库、网络、文件系统——隔离开来测试。它与 CMake 集成良好，并可以通过任何一个流行的包管理器引入。

* :arrow_forward: **Catch2**

    网址：https://github.com/catchorg/Catch2  
    价格：免费

    一个比 GoogleTest 更轻量、语法更简洁的替代品。这里的一个测试就是一个普通函数，用一个 `REQUIRE` 宏，而不是一整套专门的比较宏。它是小型项目和入门单元测试的好选择：只需引入一个头文件即可。

* :arrow_forward: **Google Benchmark**

    网址：https://github.com/google/benchmark  
    价格：免费

    一个用于微基准测试的库。它会自己挑选重复次数，让结果具有统计意义，还能对抗优化器把"结果从未被使用的代码"直接丢弃的倾向。当你需要比较两种实现的速度时就用得上它："手动"地在前后读一下时间几乎总会给出不可靠的结果。

## :robot: AI 工具

AI 助手已经成为开发者日常工具的一部分：它们加快样板代码的编写、帮你熟悉陌生的代码库、并解释编译器错误。同时，它们并不能取代对语言的了解——下面详细说明原因。

* :arrow_forward: **GitHub Copilot**

    网址：https://github.com/features/copilot  
    价格：有带限制的免费档；完整功能付费，对学生、教师以及流行开源项目的维护者免费

    直接在编辑器里补全代码：它根据文件和项目的上下文提示接下来的几行。它与 Visual Studio、VS Code、CLion 以及其他流行 IDE 集成。

* :arrow_forward: **Claude Code**

    网址：https://claude.com/product/claude-code  
    价格：付费，包含在订阅中

    一个在终端和 IDE 中工作的助手：它读取整个项目、一次性修改多个文件、运行构建和测试。它面向的是比单行更大的任务——重构、理解陌生代码、编写测试。

* :arrow_forward: **Cursor**

    网址：https://cursor.com  
    价格：有免费档，进阶功能付费

    一个基于 VS Code、内置 AI 助手的编辑器。它能回答关于代码库的问题、一次性在多个文件里做修改，同时保留你熟悉的 VS Code 扩展和设置。

* :arrow_forward: **本地模型（Ollama、llama.cpp）**

    网址：https://ollama.com, https://github.com/ggml-org/llama.cpp  
    价格：免费

    在你自己的机器上运行模型。它们在质量上不及云端模型，并且需要相当的资源，但代码不会离开你的电脑。对于禁止把源码发送到外部服务的项目来说，这是一个选择。顺便一提，`llama.cpp` 本身就是一个很有代表性的现代 C++ 项目范例。

### :warning: 需要记住的几点

- **验证一切生成的内容。** 模型可能给出看似合理却错误的代码：不存在的标准库函数、微妙的对象生命周期错误、竞态条件。在 C++ 中这类错误的代价很高——未定义行为可能不会在任何测试中暴露，却会在用户那里爆发。正因如此，对语言的了解仍然是必需的：要检验一个答案，你对这个主题的理解必须不亚于手写代码时。
- **遵守公司政策。** 在许多组织里，把工作代码发送到外部服务是受限或被禁止的。在接入助手**之前**弄清规则，而不是之后。
- **记住许可问题。** 生成的代码可能连同许可义务一起，重现别人项目的片段。对商业项目来说这是一个单独的风险，值得与团队讨论。
- **别跳过学习阶段。** 助手把你从重复劳动中解放出来，但如果它替你解决了那些你本该从中学习的问题，你作为工程师就不会成长。在职业生涯早期，先自己解决问题、然后再和模型给出的方案作对比，是有益的。

## :floppy_disk: Git 客户端

* :arrow_forward: **SmartGit**

    网址：https://www.syntevo.com/smartgit/  
    价格：开源免费

    一个完整的、跨平台的用于处理 Git 仓库的工具。开箱即用，提供以下功能：接收和发送对仓库的更改，查看更改历史记录，文本编辑器以解决冲突等。支持与所有流行的代码托管服务集成，如 GitHub、BitBucket、GitLab 等。

* :arrow_forward: **Atlassian SourceTree**

    网址：https://www.sourcetreeapp.com/  
    价格：免费

  一个很好的免费替代品，使用图形界面来处理 Git。它具有与 SmartGit 相同的功能，唯一不同之处是没有自己的编辑器用于冲突解决。但是，可以通过集成 Visual Studio Code 或任何其他可以比较文件的编辑器轻松解决此问题。请注意，与 SmartGit 不同，它仅适用于 Windows 和 macOS。它支持与流行存储库（如 GitHub、BitBucket、GitLab 等）集成。

* :arrow_forward: **Git Kraken**

    网址：https://www.gitkraken.com/  
    价格：开源免费

    一款跨平台高效的客户端，适用于 Windows、Linux 和 MacOS。它支持与 GitHub、Bitbucket 和 Gitlab 集成，并具有日常工作所需的所有必要功能，如查看更改历史记录、提交和接收更改、在分支之间切换以及内置冲突解决编辑器。

---

[**回到主页**](README.md)
