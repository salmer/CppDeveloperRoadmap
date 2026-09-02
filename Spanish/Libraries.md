# :package: Bibliotecas y frameworks populares

C++ no tiene un ecosistema único "estándar" como npm en JavaScript o crates.io en Rust, por lo que el conjunto de bibliotecas en uso depende en gran medida del dominio. Aun así, hay algunos nombres que aparecen en las ofertas de trabajo y en los proyectos con más frecuencia que el resto, y esos son los que se recopilan a continuación.

No intentes aprender todo a la vez. Es mucho más útil sentirse realmente cómodo con una o dos bibliotecas de tu propio campo que conocer una docena superficialmente. La forma más sencilla de incorporarlas es a través de los gestores de paquetes Conan o vcpkg: consulta el [Conjunto de herramientas del lenguaje](../English/Tooling.md).

> :compass: Este es un artículo de descripción general y un punto de partida para la navegación, no un catálogo completo. La cantidad de bibliotecas que existen realmente es de órdenes de magnitud mayor, y para cualquier tarea específica casi siempre hay algo más por ahí: busca dentro de tu propio dominio de problemas, mira qué usan proyectos similares y verifica las listas actualizadas (por ejemplo, [awesome-cpp](https://github.com/fffaraz/awesome-cpp)). El objetivo de esta lista es dar un punto de apoyo a aquellos que recién están comenzando.

> :bulb: Las herramientas de desarrollo (compiladores, depuradores, analizadores, frameworks de pruebas) están cubiertas en un artículo separado: [Conjunto de herramientas del lenguaje](../English/Tooling.md).

## :hammer_and_wrench: Propósito general

* :arrow_forward: **Boost** - [boost.org](https://www.boost.org)

    Una gran colección de bibliotecas que históricamente ha servido como un "campo de pruebas" para la biblioteca estándar: gran parte de lo que hoy forma parte del estándar (smart pointers, `filesystem`, `optional`, `variant`) se probó por primera vez en Boost. Todavía es útil ahora: contiene cosas de las que el estándar aún carece. La otra cara de la moneda es el tamaño: incorporar todo Boost por el bien de una función es una mala idea; la mayoría de sus bibliotecas se pueden tomar por separado.

* :arrow_forward: **{fmt}** - [github.com/fmtlib/fmt](https://github.com/fmtlib/fmt)

    Una biblioteca de formato de cadenas que se convirtió en la base de `std::format` en C++20. Más rápida y segura que `printf`, más legible que los flujos (streams) de `iostream`. Tiene sentido si tu compilador aún no soporta `std::format` o si necesitas capacidades más allá del estándar.

* :arrow_forward: **spdlog** - [github.com/gabime/spdlog](https://github.com/gabime/spdlog)

    Una biblioteca de registro (logging) rápida construida sobre {fmt}. Soporta la salida a archivos con rotación, a una consola con resaltado y un modo asincrónico. El registro es una de las principales herramientas de diagnóstico en producción, cuando adjuntar un depurador (debugger) es imposible.

* :arrow_forward: **range-v3** - [github.com/ericniebler/range-v3](https://github.com/ericniebler/range-v3)

    La implementación de referencia en la que se basó `std::ranges` en C++20. Te permite escribir transformaciones de secuencias como una cadena, sin iteradores explícitos ni contenedores temporales. Es relevante si necesitas funciones que aún no han llegado al estándar o soporte para compiladores más antiguos.

## :globe_with_meridians: Redes e intercambio de datos

* :arrow_forward: **Asio** - [think-async.com/Asio](https://think-async.com/Asio/)

    El estándar de facto para la E/S asincrónica en C++ y la base de muchos proyectos de red. Existe en dos variantes: como una biblioteca independiente y como parte de Boost. Funciona bien con corrutinas de C++20. Sobre su base se ha propuesto repetidamente una biblioteca de red para el estándar.

* :arrow_forward: **nlohmann/json** - [github.com/nlohmann/json](https://github.com/nlohmann/json)

    La biblioteca más popular para trabajar con JSON en C++. Se valora por el hecho de que el código que la usa se ve casi como un lenguaje con soporte JSON integrado. Se incorpora como un solo archivo de encabezado (header). Si la velocidad de análisis en grandes volúmenes es crítica, vale la pena considerar alternativas más rápidas como simdjson o RapidJSON.

* :arrow_forward: **Protocol Buffers** - [protobuf.dev](https://protobuf.dev)

    Un formato de serialización binaria basado en esquemas de Google: la estructura de datos se describe en un archivo separado, a partir del cual se genera el código. Más compacto y más rápido que JSON, y el esquema brinda control sobre la compatibilidad de versiones, una propiedad importante cuando el cliente y el servidor no se actualizan al mismo tiempo.

* :arrow_forward: **gRPC** - [grpc.io](https://grpc.io)

    Un framework de llamadas a procedimientos remotos sobre Protocol Buffers y HTTP/2. Está muy extendido en las arquitecturas de microservicios, incluidas las configuraciones donde los servicios están escritos en diferentes lenguajes.

* :arrow_forward: **POCO** - [pocoproject.org](https://pocoproject.org)

    Un conjunto de bibliotecas multiplataforma para aplicaciones en red y de servidor: un cliente y servidor HTTP, acceso a bases de datos, análisis de XML y JSON, registro (logging). En espíritu, está más cerca de "baterías incluidas" que de un conjunto de bibliotecas específicas.

## :framed_picture: Interfaz gráfica de usuario

* :arrow_forward: **Qt** - [qt.io](https://www.qt.io)

    El framework más extendido para aplicaciones de escritorio en C++, que hace mucho tiempo superó los límites de una GUI: incluye redes, bases de datos, hilos (threads) y análisis de formatos. Es multiplataforma, con su propio IDE (Qt Creator). Un matiz importante es la licencia: la versión abierta se distribuye bajo LGPL/GPL, y un producto comercial cerrado puede requerir una licencia paga. Vale la pena estudiar los términos **antes** de comenzar el desarrollo.

## :bar_chart: Computación, gráficos y aprendizaje automático

* :arrow_forward: **OpenCV** - [opencv.org](https://opencv.org)

    El estándar de facto en visión por computadora: procesamiento de imágenes y videos, detección de objetos, calibración de cámaras. Se utiliza en robótica, control de calidad industrial e imágenes médicas.

* :arrow_forward: **Eigen** - [libeigen.gitlab.io](https://libeigen.gitlab.io/)

    Una biblioteca de álgebra lineal: matrices, vectores, resolución de sistemas de ecuaciones. Consta solo de archivos de encabezado y está agresivamente optimizada. Aparece a menudo en robótica, simulaciones y visión por computadora.

* :arrow_forward: **CUDA** - [developer.nvidia.com/cuda-toolkit](https://developer.nvidia.com/cuda-toolkit) y **OpenCL** - [khronos.org/opencl](https://www.khronos.org/opencl/)

    Dos enfoques de computación en tarjetas gráficas. CUDA se ejecuta solo en hardware NVIDIA pero es más maduro y conveniente; OpenCL es un estándar abierto que funciona en hardware de varios proveedores. Tienen demanda cuando una tarea se paraleliza bien: computación científica, procesamiento de imágenes, aprendizaje automático.

* :arrow_forward: **LibTorch (PyTorch C++)** - [pytorch.org/cppdocs](https://pytorch.org/cppdocs/) y **TensorFlow** - [tensorflow.org](https://www.tensorflow.org)

    Las API de C++ de los dos principales frameworks de aprendizaje automático. El entrenamiento del modelo generalmente se realiza en Python, mientras que C++ se usa en la etapa de implementación: cuando un modelo terminado necesita ejecutarse dentro de una aplicación con requisitos de velocidad estrictos o sin depender de Python.

## :link: Interoperabilidad con otros lenguajes

* :arrow_forward: **pybind11** - [github.com/pybind/pybind11](https://github.com/pybind/pybind11)

    Te permite convertir el código C++ en un módulo importable en Python. El escenario típico: la computación pesada está escrita en C++, mientras que la lógica de nivel superior y los experimentos se quedan en Python. Los envoltorios (wrappers) de muchos proyectos conocidos están basados en pybind11.

---

[**A la página principal**](README.md)
