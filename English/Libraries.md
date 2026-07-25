# :package: Popular libraries and frameworks

C++ has no single "standard" ecosystem like npm in JavaScript or crates.io in Rust, so the set of libraries in use depends heavily on the domain. Even so, there are a few names that show up in job postings and on projects more often than the rest — and those are the ones collected below.

Do not try to learn everything at once. It is far more useful to get really comfortable with one or two libraries from your own field than to know a dozen superficially. The easiest way to pull them in is through the Conan or vcpkg package managers — see [Language toolkit](Tooling.md).

> :compass: This is an overview article and a starting point for navigation, not a complete catalog. The number of libraries that actually exist is orders of magnitude larger, and for any specific task there is almost always something else out there — search within your own problem domain, look at what similar projects use, and check against fresh, up-to-date lists (for example, [awesome-cpp](https://github.com/fffaraz/awesome-cpp)). The goal of this list is to give a foothold to those who are just starting out.

> :bulb: Development tools (compilers, debuggers, analyzers, testing frameworks) are covered in a separate article — [Language toolkit](Tooling.md).

## :hammer_and_wrench: General purpose

* :arrow_forward: **Boost** - [boost.org](https://www.boost.org)

    A huge collection of libraries that has historically served as a "proving ground" for the standard library: much of what is part of the standard today (smart pointers, `filesystem`, `optional`, `variant`) was first road-tested in Boost. It is still useful now — it contains things the standard still lacks. The flip side is size: pulling in all of Boost for the sake of one function is a bad idea; most of its libraries can be taken separately.

* :arrow_forward: **{fmt}** - [github.com/fmtlib/fmt](https://github.com/fmtlib/fmt)

    A string-formatting library that became the basis for `std::format` in C++20. Faster and safer than `printf`, more readable than `iostream` streams. It makes sense if your compiler does not yet support `std::format` or you need capabilities beyond the standard.

* :arrow_forward: **spdlog** - [github.com/gabime/spdlog](https://github.com/gabime/spdlog)

    A fast logging library built on top of {fmt}. It supports output to files with rotation, to a console with highlighting, and an asynchronous mode. Logging is one of the main diagnostic tools in production, when attaching a debugger is impossible.

* :arrow_forward: **range-v3** - [github.com/ericniebler/range-v3](https://github.com/ericniebler/range-v3)

    The reference implementation on which `std::ranges` in C++20 was based. It lets you write sequence transformations as a chain, without explicit iterators and temporary containers. It is relevant if you need features that have not yet made it into the standard, or support for older compilers.

## :globe_with_meridians: Networking and data exchange

* :arrow_forward: **Asio** - [think-async.com/Asio](https://think-async.com/Asio/)

    The de facto standard for asynchronous I/O in C++ and the foundation of many networking projects. It exists in two variants: as a standalone library and as part of Boost. It works well with C++20 coroutines. It is on its basis that a networking library for the standard has repeatedly been proposed.

* :arrow_forward: **nlohmann/json** - [github.com/nlohmann/json](https://github.com/nlohmann/json)

    The most popular library for working with JSON in C++. It is valued for the fact that code using it looks almost like a language with built-in JSON support. It is pulled in as a single header file. If parsing speed on large volumes is critical, it is worth looking at faster alternatives such as simdjson or RapidJSON.

* :arrow_forward: **Protocol Buffers** - [protobuf.dev](https://protobuf.dev)

    A schema-based binary serialization format from Google: the data structure is described in a separate file, from which code is generated. More compact and faster than JSON, and the schema gives control over version compatibility — an important property when the client and server are not updated at the same time.

* :arrow_forward: **gRPC** - [grpc.io](https://grpc.io)

    A remote procedure call framework on top of Protocol Buffers and HTTP/2. It is widespread in microservice architectures, including setups where services are written in different languages.

* :arrow_forward: **POCO** - [pocoproject.org](https://pocoproject.org)

    A set of cross-platform libraries for networked and server applications: an HTTP client and server, database access, XML and JSON parsing, logging. In spirit it is closer to "batteries included" than to a set of pinpoint libraries.

## :framed_picture: Graphical user interface

* :arrow_forward: **Qt** - [qt.io](https://www.qt.io)

    The most widespread framework for desktop applications in C++, long since outgrown the bounds of a GUI: it includes networking, databases, threads, and format parsing. It is cross-platform, with its own IDE (Qt Creator). An important nuance is licensing: the open version is distributed under LGPL/GPL, and a closed commercial product may require a paid license. The terms are worth studying **before** you start development.

## :bar_chart: Computation, graphics, and machine learning

* :arrow_forward: **OpenCV** - [opencv.org](https://opencv.org)

    The de facto standard in computer vision: image and video processing, object detection, camera calibration. It is used in robotics, industrial quality control, and medical imaging.

* :arrow_forward: **Eigen** - [libeigen.gitlab.io](https://libeigen.gitlab.io/)

    A linear-algebra library: matrices, vectors, solving systems of equations. It consists of header files only and is aggressively optimized. It shows up often in robotics, simulations, and computer vision.

* :arrow_forward: **CUDA** - [developer.nvidia.com/cuda-toolkit](https://developer.nvidia.com/cuda-toolkit) and **OpenCL** - [khronos.org/opencl](https://www.khronos.org/opencl/)

    Two approaches to computing on graphics cards. CUDA runs only on NVIDIA hardware but is more mature and convenient; OpenCL is an open standard that works on hardware from various vendors. They are in demand where a task parallelizes well: scientific computing, image processing, machine learning.

* :arrow_forward: **LibTorch (PyTorch C++)** - [pytorch.org/cppdocs](https://pytorch.org/cppdocs/) and **TensorFlow** - [tensorflow.org](https://www.tensorflow.org)

    The C++ APIs of the two main machine-learning frameworks. Model training is usually done in Python, while C++ is used at the deployment stage: when a finished model needs to run inside an application with strict speed requirements or without a dependency on Python.

## :link: Interoperability with other languages

* :arrow_forward: **pybind11** - [github.com/pybind/pybind11](https://github.com/pybind/pybind11)

    It lets you turn C++ code into a module importable into Python. The typical scenario: heavy computation is written in C++, while the top-level logic and experiments stay in Python. Many well-known projects' wrappers are built on pybind11.

---

[**To main page**](../README.md)
