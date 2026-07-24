# :triangular_ruler: Language toolkit

Newborn developers often have a limited understanding of the tools available to make working with code easier, increase efficiency, and protect against many mistakes. These tools are not a silver bullet for the difficulties the language may present, but they can significantly smooth out the rough edges. The following is a list of common and popular tools recognized by developers around the world, but it is only a small portion of what is available. Over time, you will become more familiar with these tools and discover new ones that suit your needs.

## :gear: Compilers

* :arrow_forward: **GCC (GNU Compiler Collection)**

    Site: https://gcc.gnu.org

    Price: free

    The default compiler on most Linux distributions and one of the most widely used C++ compilers in the world. It closely tracks the latest language standards and produces highly optimized code. On Windows, it is available through the MSYS2 and MinGW-w64 projects.

* :arrow_forward: **Clang**

    Site: https://clang.llvm.org

    Price: free

    A compiler built on the LLVM infrastructure and the default compiler on macOS. It is known for fast compilation and clear, human-friendly error messages, which makes it a good choice for beginners. Clang is also the foundation of a whole family of developer tools, such as clang-format, clang-tidy, and the clangd language server used by many editors.

* :arrow_forward: **MSVC (Microsoft Visual C++)**

    Site: https://visualstudio.microsoft.com

    Price: included in Visual Studio (Community Edition is free)

    Microsoft's compiler, shipped as part of Visual Studio, and the primary choice for Windows development. Most commercial Windows software and game projects are built with it.

    **Tip:** You can quickly try your code on all three compilers side by side without installing anything using [Compiler Explorer](https://godbolt.org).

## :page_facing_up: Text editors

* :arrow_forward: **Visual Studio Code**

    Site: https://code.visualstudio.com/

    Price: free

    A powerful and efficient editor for text files and source code is available. It has a rich library of extensions that enables customization for personal preferences. It can also be configured to work with source code, allowing you to compile, run, and debug your code with ease. Additionally, it has a powerful search engine for files and folders, making it easier to search, read, and work with large projects.


* :arrow_forward: **Notepad++**

    Site: https://notepad-plus-plus.org/

    Price: free

    A lightweight editor for text files and source code, it supports syntax highlighting for common programming languages. Compared to Visual Studio Code, it is more convenient for quickly opening and viewing files and due to its lightweight design, it is comfortable to work with a large number of text files.


## :open_file_folder: IDE (Integrated Development Environment)

* :arrow_forward: **Microsoft Visual Studio IDE**

    Site: https://visualstudio.microsoft.com

    Price: Community Edition is free

    An integrated development environment (IDE) from Microsoft, providing a comprehensive set of tools including a code editor, compiler, debugger, and profiler, for various programming languages and cross-platform development. A great option for beginners, as its modern interface is user-friendly and requires minimal customization out of the box.


* :arrow_forward: **Qt Creator IDE**

    Site: https://www.qt.io/product/development-tools
    
    Price: free for open source projects (more details: [Qt Open Source](https://www.qt.io/download-open-source?hsCtaTracking=9f6a2170-a938-42df-a8e2-a9f0b1d6cdce%7C6cb0de4f-9bb5-4778-ab02-bfb62735f3e5))

    Initially, Qt Creator was positioned as an IDE for developing graphical interfaces for C++ applications. Over time, the framework has acquired numerous capabilities and evolved into a comprehensive ecosystem for cross-platform development. It offers a vast library of primitives for various needs such as networking, graphical interface, database work, and handling popular formats like images and text files. Today, Qt Creator serves as a competitor to Visual Studio and is particularly popular among developers creating applications for various Linux distributions.


* :arrow_forward: **Xcode**

    Site: https://developer.apple.com/xcode/

    Price: free

    Apple's own development environment and the only way to build applications for macOS and iOS. It ships with Clang and LLDB. If you work on macOS, you will need Xcode at least for its command-line tools, even if you prefer to write code in a different editor.


* :arrow_forward: **JetBrains CLion IDE**

    Site: https://www.jetbrains.com/clion

    Price: free for non-commercial use (since May 2025); paid license required for commercial development

    Powerful multi-platform IDE from JetBrains. Like other IDEs, it provides a comprehensive set of tools for comfortable software development. It is convenient for cross-platform development in both C and C++.

## :flashlight: Extensions

* :arrow_forward: **JetBrains ReSharper C++**

    Site: https://www.jetbrains.com/resharper-cpp

    Price: free for students and teachers

    An extension for Microsoft Visual Studio, it adds advanced features for working with source code such as extended code highlighting and hints, building dependency diagrams between projects, recommendations for correcting common errors in code, enhanced information during debugging, improved searching and navigating within projects, etc. It competes with Visual Assist.

* :arrow_forward: **Visual Assist**

    Site: https://www.wholetomato.com

    An extension for Microsoft Visual Studio that provides additional features for working with source code, such as enhanced code highlighting and hints, increased information during debugging and coding, advanced search capabilities, and improved project navigation. It competes with JetBrains ReSharper.


* :arrow_forward: **Incredibuild**

    Site: https://www.incredibuild.com

    Price: have to contact incredibuild team to find the price

    Application/extension for distributed compilation of projects, which unites all developer workstations into a single network, providing the possibility of using dozens of machines to assemble and compile the source code. This speeds up the build process for large projects.

## :electric_plug: Package managers and build systems

* :arrow_forward: **CMake**

    Site: https://cmake.org

    Price: free

    A cross-platform automation system for building an application from source code, which generates the necessary artifacts for subsequent assembly on the target platform. It is currently considered the standard tool for building various libraries when supplied as source.

* :arrow_forward: **Conan**

    Site: https://conan.io

    Price: free

    A package manager and dependency manager for organizing C++ libraries and frameworks. It supports work on various platforms such as Windows and Linux, and has integration with tools such as CMake and Visual Studio.

* :arrow_forward: **vcpkg**

    Site: https://vcpkg.io

    Price: free

    A free and open-source package manager for C and C++ libraries, developed by Microsoft. It provides thousands of ready-to-use libraries and integrates smoothly with CMake and Visual Studio. Together with Conan, it is one of the two most popular dependency managers in the C++ ecosystem.


* :arrow_forward: **Ninja**

    Site: https://ninja-build.org

    Price: free

    Project build manager for C and C++ applications. The main advantage of this manager is quick project assembly. It supports cross-platform development and works with all popular compilers.

* :arrow_forward: **ccache**

    Site: https://ccache.dev

    Price: free

    A compiler cache: it stores the results of previous compilations and reuses them when the same compilation happens again, which can dramatically speed up rebuilds. It sits transparently in front of GCC or Clang and integrates with CMake in a couple of lines, making it one of the cheapest build-time wins on medium and large projects.


## :mag: Code analyzers and formatters

* :arrow_forward: **clang-format**

    Site: https://clang.llvm.org/docs/ClangFormat.html

    Price: free

    The de-facto standard automatic code formatter for C++. A single configuration file (`.clang-format`) stored in the repository keeps the whole team's code style consistent and removes formatting debates from code review. It is supported out of the box by virtually all editors and IDEs.

* :arrow_forward: **clang-tidy**

    Site: https://clang.llvm.org/extra/clang-tidy/

    Price: free

    A static analysis tool (linter) from the LLVM project. It checks code against hundreds of rules — bug-prone patterns, performance issues, readability, modern C++ style — and can automatically fix many of the problems it finds. It is integrated into most IDEs, including Visual Studio, CLion, VS Code, and Qt Creator.

* :arrow_forward: **Sanitizers (ASan, UBSan, TSan)**

    Site: https://github.com/google/sanitizers

    Price: free

    Dynamic analysis tools built directly into GCC, Clang, and MSVC and enabled with compiler flags (e.g. `-fsanitize=address`). AddressSanitizer catches memory errors such as out-of-bounds access and use-after-free, UndefinedBehaviorSanitizer catches undefined behavior, and ThreadSanitizer catches data races. Running your tests with sanitizers enabled is considered a baseline practice in modern C++ development.

* :arrow_forward: **Fuzzing (libFuzzer, AFL++)**

    Site: https://llvm.org/docs/LibFuzzer.html, https://github.com/AFLplusplus/AFLplusplus

    Price: free

    Fuzzing is the automatic feeding of a stream of random and deliberately malformed data into your code in search of crashes and hangs. It is especially useful for anything that parses external input: format parsers, network protocols, decoders. It is usually run together with sanitizers — the fuzzer finds the input that triggers an error, and the sanitizer shows exactly where it occurred. libFuzzer is built into Clang; AFL++ works as a standalone tool.

* :arrow_forward: **PVS Studio**

    Site: https://pvs-studio.com

    Price: paid; free for open-source projects and students

    Cross-platform (Windows, Linux, MacOS) static code analyzer by PVS-Studio. The main aim of the analyzer is to analyze the source code for various errors that may go undetected by compilers or during code review. It helps reduce the number of errors related to language syntax and pitfalls.


* :arrow_forward: **Cppcheck**

    Site: https://cppcheck.sourceforge.io

    Price: free

    A free code analyzer that helps you catch common errors in your source code that might be missed by the compiler or during code review. It is cross-platform and supports popular Linux distributions and Windows.


* :arrow_forward: **Valgrind**

    Site: https://valgrind.org

    Price: free

    A set of tools that can help you investigate various problems while the application is running, such as memory leaks and performance profiling. It is compatible with multiple Linux distributions. On modern projects, sanitizers cover many of the same use cases with much lower overhead, but Valgrind remains useful because it requires no recompilation.

## :beetle: Debuggers

* :arrow_forward: **GDB (GNU Debugger)**

    Site: https://sourceware.org/gdb/

    Price: free

    The standard debugger in the GNU/Linux world. It lets you set breakpoints, step through code, inspect variables and memory, and analyze core dumps of crashed applications. Most IDE debugging front-ends on Linux (VS Code, Qt Creator, CLion) use GDB under the hood, so understanding its basics pays off even if you mostly debug from an IDE.

* :arrow_forward: **LLDB**

    Site: https://lldb.llvm.org

    Price: free

    The debugger from the LLVM project and the default debugger on macOS (used by Xcode). It offers capabilities similar to GDB with a more modern architecture.

* :arrow_forward: **WinDbg**

    Site: https://learn.microsoft.com/windows-hardware/drivers/debugger/

    Price: free

    Microsoft's debugger for Windows. For everyday work on Windows the debugger built into Visual Studio is usually enough, but WinDbg is indispensable where its capabilities fall short: analyzing crash dumps from production machines, debugging drivers and kernel mode, working with an application without source. A useful skill for anyone doing low-level development or investigating crashes on users' machines.

## :stopwatch: Profilers

* :arrow_forward: **perf**

    Site: https://perfwiki.github.io/main/

    Price: free

    The standard sampling profiler on Linux, built into the kernel. It shows where an application actually spends its CPU time, with hardware-counter details (cache misses, branch mispredictions) when you need them. Often used together with flame-graph visualizations to make hotspots obvious.

* :arrow_forward: **Tracy**

    Site: https://github.com/wolfpld/tracy

    Price: free

    A real-time frame profiler that is especially popular in game development. You annotate zones in your code with lightweight macros and watch timings live in a graphical client, down to individual frames and threads. Cross-platform and remarkably low-overhead.

* :arrow_forward: **Intel VTune Profiler**

    Site: https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html

    Price: free

    A powerful profiler for deep performance analysis on x86: hotspots, threading efficiency, memory access patterns, and microarchitecture-level metrics. The go-to tool when `perf` output is not detailed enough. On Windows, the Visual Studio IDE also ships a capable built-in CPU and memory profiler.

## :white_check_mark: Testing and benchmarks

* :arrow_forward: **GoogleTest (gtest/gmock)**

    Site: https://github.com/google/googletest

    Price: free

    The most widely used unit-testing framework in C++. It comes with GoogleMock for creating stubs and mocks, which lets you test code in isolation from its dependencies — databases, the network, the file system. It integrates well with CMake and can be pulled in through any of the popular package managers.

* :arrow_forward: **Catch2**

    Site: https://github.com/catchorg/Catch2

    Price: free

    A lighter alternative to GoogleTest with a concise syntax. A test here is an ordinary function with a `REQUIRE` macro instead of a set of special comparison macros. A good choice for small projects and for getting acquainted with unit testing: it can be pulled in as a single header file.

* :arrow_forward: **Google Benchmark**

    Site: https://github.com/google/benchmark

    Price: free

    A library for microbenchmarks. It picks the number of repetitions itself so that the result is statistically significant, and it can fight the optimizer's tendency to throw away code whose result is never used. It is needed where you have to compare two implementations by speed: timing "by hand" with a clock reading before and after almost always gives an unreliable result.

## :robot: AI tools

AI assistants have become part of a developer's everyday toolkit: they speed up writing boilerplate code, help you find your way around an unfamiliar codebase, and explain compiler errors. At the same time, they do not replace knowledge of the language — the reasons why are spelled out below.

* :arrow_forward: **GitHub Copilot**

    Site: https://github.com/features/copilot

    Price: there is a limited free tier; full access is paid, and free for students, teachers, and maintainers of popular open source projects

    Code completion right in the editor: it suggests the next lines based on the context of the file and project. It integrates with Visual Studio, VS Code, CLion, and other popular IDEs.

* :arrow_forward: **Claude Code**

    Site: https://claude.com/product/claude-code

    Price: paid, as part of a subscription

    An assistant that works in the terminal and in the IDE: it reads the whole project, makes edits across several files at once, and runs the build and tests. It is aimed at tasks larger than a single line — refactoring, exploring unfamiliar code, writing tests.

* :arrow_forward: **Cursor**

    Site: https://cursor.com

    Price: there is a free tier; advanced features are paid

    An editor based on VS Code with a built-in AI assistant. It can answer questions about the codebase and make edits across several files at once, while keeping the familiar VS Code extensions and settings.

* :arrow_forward: **Local models (Ollama, llama.cpp)**

    Site: https://ollama.com, https://github.com/ggml-org/llama.cpp

    Price: free

    Running models on your own machine. They are inferior to cloud models in quality and require noticeable resources, but the code never leaves your computer. This is an option for projects where sending source to external services is forbidden. Incidentally, `llama.cpp` is itself an instructive example of a modern C++ project.

### :warning: What to keep in mind

- **Verify everything that is generated.** A model can produce plausible but incorrect code: nonexistent standard-library functions, subtle object-lifetime bugs, race conditions. In C++ the cost of such a mistake is high — undefined behavior may not show up in any test and may blow up on a user's machine. This is exactly why knowledge of the language remains mandatory: to check an answer, you need to understand the subject no worse than you would when writing the code by hand.
- **Follow company policy.** In many organizations, sending work code to external services is restricted or forbidden. Clarify the rules before you connect an assistant, not after.
- **Remember licensing.** Generated code may reproduce fragments of other people's projects along with their licensing obligations. For commercial projects this is a separate risk worth discussing with your team.
- **Do not skip the learning stage.** An assistant frees you from routine, but if it solves for you the very problems you are supposed to be learning from, you will not grow as an engineer. Early in your career it is useful to solve a problem yourself first and only then compare it with what the model suggests.

## :floppy_disk: Git clients

* :arrow_forward: **SmartGit**

    Site: https://www.syntevo.com/smartgit/

    Price: free for open source projects

    A complete, cross-platform tool for working with Git repositories. Out of the box, it provides the following features: receiving and sending changes to the repository, viewing the history of changes, a text editor for resolving conflicts, etc. Supports integration with all popular repositories like GitHub, BitBucket, GitLab, etc.

* :arrow_forward: **Atlassian SourceTree**

    Site: https://www.sourcetreeapp.com/

    Price: free

    A great free alternative for working with Git using a GUI. It has the same functionality as SmartGit, with the exception of the absence of its own editor for conflict resolution. However, this can be easily fixed by integrating Visual Studio Code or any other editor that can compare files. Note that unlike SmartGit, it is only available for Windows and macOS. It supports integration with popular repositories such as GitHub, BitBucket, GitLab, etc.


* :arrow_forward: **Git Kraken**

    Site: https://www.gitkraken.com/

    Price: free for open source projects

    A cross-platform and highly efficient client for Windows, Linux, and MacOS. It supports integration with GitHub, Bitbucket, and Gitlab, and has all the necessary functionality for everyday work, such as viewing the change history, submitting and receiving changes, switching between branches, and a built-in conflict resolution editor.

---

[**To main page**](../README.md)
