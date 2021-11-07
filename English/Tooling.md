# Language toolkit

Newborn developers have a limited understanding of the tools available, which make it easier to work with code, as well as increase efficiency and protect against many mistakes. All these tools are not a silver bullet for difficulties that language has for you, but they significantly smooth out the corners. Below is a list of common and popular tools recognized by developers around the world. This list is only a small part of the available tools. Over time, you will begin to better navigate them and find something new for yourself.

## Text editors

* **Visual Studio Code**

    Site: https://code.visualstudio.com/

    Price: free

    Powerful and efficient editor for text files and source code. Has a rich library of extensions that will allow you to customize it for yourself. It is also possible to customize it to work with source code: compile, run and debug. It has a powerful search engine for files and folders, which increases the efficiency of searching, reading and working with large projects.


* **Notepad++**

    Site: https://notepad-plus-plus.org/

    Price: free

    Lightweight editor for text files and source code. Supports syntax and highlighting of common programming languages. Compared to Visual Studio Code, it is convenient to use for quickly opening and viewing files. Due to its lightness, it is comfortable to work with a large number of text files. 


## IDE (Integrated Development Environment)

* **Microsoft Visual Studio IDE**

    Site: https://visualstudio.microsoft.com

    Price: Community Edition is free

    Integrated development environment from Microsoft. Provides all the necessary set of tools (code editor, compiler, debugger, profiler, etc.) out of the box. Supports development in various programming languages as well as cross-platform development. A great start for newbies as the modern interface of the studio is as friendly as possible, and practically does not require any adjustment out of the box.


* **Qt Creator IDE**

    Site: https://www.qt.io/product/development-tools
    
    Price: free for open source projects (more details: [Qt Open Source](https://www.qt.io/download-open-source?hsCtaTracking=9f6a2170-a938-42df-a8e2-a9f0b1d6cdce%7C6cb0de4f-9bb5-4778-ab02-bfb62735f3e5))

    Initially, Qt Creator was positioned as an IDE for developing graphical interfaces for applications in C++. But over the time, the framework has acquired tremendous opportunities. As a result, the framework has grown into a full-fledged ecosystem for developing cross-platform applications. It provides a large library of primitives for various needs: networking, graphical interface, database work, work with popular formats: images, text files, etc. Modern Qt Creator acts as a competitor for Visual Studio, but mostly it has gained developers who develop applications for various Linux distributions. 


* **Eclipse IDE**

    Site: https://www.eclipse.org/downloads/packages

    Price: free
    
    Quite a powerful multi-platform development environment, but at the same time heavyweight. A key feature of Eclipse is modularity. The philosophy of Eclipse is that any developer can modify the development environment for himself by connecting additional extensions. Taken as a basis by some compiler developers for specialized OS or microcontrollers (for example: QNX real-time OS).


* **JetBrains Clion IDE**

    Site: https://www.jetbrains.com/clion

    Price: free for students and teachers

    Powerful multiplatform IDE from Russian company JetBrains. Like other IDEs, it contains a complete set of tools for comfortable software development. Convenient for cross-platform development in both C and C++.

## Extensions

* **JetBrains ReSharper C++**

    Site: https://www.jetbrains.com/resharper-cpp

    Price: free for students and teachers

    Extension for MS Visual Studio. Adds additional features for working with source code: extended highlighting of the code and hints on it, building dependency diagrams between projects, recommendations on common errors in the code and how to improve it, extended information during debugging, advanced search, project navigation, etc. It is a competitor to Visual Assist.

* **Visual Assist**

    Site: https://www.wholetomato.com

    Extension for MS Visual Studio. Adds additional features for working with source code: extended code highlighting and hints on it, extended information during debugging or when writing code, advanced search, project navigation, etc. It is a competitor to JetBrains ReSharper.


* **Incredibuild**

    Site: https://www.incredibuild.com

    Price: have to contact incredibuild team to find the price

    Application/extension for distributed compilation of projects. It unites all dev workstations into a single network which provides a possibility to use dozens of machines to assemble and compile the source code. This allows you to speed up the build of large projects.

## Package managers and build systems

* **Cmake**

    Site: https://cmake.org

    A cross-platform automation system for building an application from source code. Generates the necessary artifacts for the subsequent assembly of the application on the target platform. It is currently considered the "standard" tool for building various libraries when supplied as source.

* **Conan**

    Site: https://conan.io

    Price: free

    A package manager as well as a dependency manager for organizing C++ libraries and frameworks. Supports work with various platforms: Windows, Linux, etc. Supports integration with CMake, Visual Studio, etc.


* **Ninja**

    Site: https://ninja-build.org

    Price: free

    Project build manager for C and C++ applications. The main advantages that this manager claims: quick project assembly. Supports cross-platform development, supports all popular compilers.


## Code analyzers

* **PVS Studio**

    Site: https://pvs-studio.com

    Price: 30 days trial

    Cross-platform (Windows, Linux, MacOS) static code analyzer from the Russian company PVS-Studio. The main task of the analyzer is to analyze the source code for various errors that are not detected by compilers or at the stage of code review. It helps to minimize number of errors associated with the syntactic structures of the language and their pitfalls.


* **Cpp Check**

    Site: https://cppcheck.sourceforge.io

    Price: free

    Free code analyzer. It will help you catch common errors by analyzing the source code, which may be missed by the compiler or during the code review process. Cross-platform, supports popular Linux distributions and Windows.


* **Valgrind**

    Site: https://www.valgrind.org

    Price: free

    A set of tools that can help you investigate a variety of problems while the application is running: memory leaks, brake profiling, etc. It suits various Linux distributions.

## Git clients

* **SmartGit**

    Site: https://www.syntevo.com/smartgit/

    Price: free for open source projects

    A complete cross-platform tool for working with git repositories. Out of the box, it provides the following features: receiving/sending changes to the repository, viewing the history of changes, a text editor for resolving conflicts, etc. Supports integration with all popular repositories: GitHub, BitBucket, GitLab, etc.

* **Atlassian SourceTree**

    Site: https://www.sourcetreeapp.com/

    Price: free

    A great free alternative for working with git using GUI. Has the same functionality as SmartGit. The only exception is absence of its own editor for conflict resolution. But this can be easily fixed by integrating Visual Code or any other editor that can compare files with each other. In all other respects, it completely duplicates the functionality of SmartGit: cross-platform, supports integration with public repositories: GitHub, BitBucket, GitLab, etc.


* **Git Kraken**

    Site: https://www.gitkraken.com/

    Price: free for open source projects

    Cross-platform and highly efficient client for Windows, Linux, MacOS. Supports integration with GitHub, Bitbucket and Gitlab, as well as all the necessary functionality for everyday work: studying the history of changes, receiving/submitting changes, switching between branches, built-in conflict resolution editor, etc.

