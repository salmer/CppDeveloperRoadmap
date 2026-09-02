# :triangular_ruler: Herramientas del lenguaje

Los desarrolladores recién nacidos a menudo tienen una comprensión limitada de las herramientas disponibles para facilitar el trabajo con el código, aumentar la eficiencia y proteger contra muchos errores. Estas herramientas no son una bala de plata para las dificultades que pueda presentar el lenguaje, pero pueden suavizar significativamente las asperezas. A continuación se muestra una lista de herramientas comunes y populares reconocidas por desarrolladores de todo el mundo, pero es solo una pequeña parte de lo que está disponible. Con el tiempo, te familiarizarás más con estas herramientas y descubrirás otras nuevas que se adapten a tus necesidades.

## :gear: Compiladores

* :arrow_forward: **GCC (GNU Compiler Collection)**

    Sitio: https://gcc.gnu.org

    Precio: gratis

    El compilador predeterminado en la mayoría de las distribuciones de Linux y uno de los compiladores de C++ más utilizados en el mundo. Sigue de cerca los últimos estándares del lenguaje y produce código altamente optimizado. En Windows, está disponible a través de los proyectos MSYS2 y MinGW-w64.

* :arrow_forward: **Clang**

    Sitio: https://clang.llvm.org

    Precio: gratis

    Un compilador construido sobre la infraestructura LLVM y el compilador predeterminado en macOS. Es conocido por su compilación rápida y mensajes de error claros y amigables para los humanos, lo que lo convierte en una buena opción para los principiantes. Clang también es la base de toda una familia de herramientas para desarrolladores, como clang-format, clang-tidy, y el servidor de lenguaje clangd utilizado por muchos editores.

* :arrow_forward: **MSVC (Microsoft Visual C++)**

    Sitio: https://visualstudio.microsoft.com

    Precio: incluido en Visual Studio (la edición Community es gratis)

    El compilador de Microsoft, que se envía como parte de Visual Studio, y la opción principal para el desarrollo en Windows. La mayoría del software comercial y los proyectos de juegos para Windows se construyen con él.

    **Consejo:** Puedes probar rápidamente tu código en los tres compiladores uno al lado del otro sin instalar nada usando [Compiler Explorer](https://godbolt.org).

## :page_facing_up: Editores de texto

* :arrow_forward: **Visual Studio Code**

    Sitio: https://code.visualstudio.com/

    Precio: gratis

    Un editor potente y eficiente para archivos de texto y código fuente está disponible. Tiene una rica biblioteca de extensiones que permite la personalización para las preferencias personales. También se puede configurar para trabajar con código fuente, permitiéndote compilar, ejecutar y depurar tu código con facilidad. Además, tiene un potente motor de búsqueda de archivos y carpetas, facilitando la búsqueda, lectura y el trabajo con grandes proyectos.


* :arrow_forward: **Notepad++**

    Sitio: https://notepad-plus-plus.org/

    Precio: gratis

    Un editor ligero para archivos de texto y código fuente, es compatible con el resaltado de sintaxis para los lenguajes de programación comunes. En comparación con Visual Studio Code, es más conveniente para abrir y ver archivos rápidamente y debido a su diseño liviano, es cómodo trabajar con una gran cantidad de archivos de texto.


## :open_file_folder: IDE (Entorno de Desarrollo Integrado)

* :arrow_forward: **Microsoft Visual Studio IDE**

    Sitio: https://visualstudio.microsoft.com

    Precio: la edición Community es gratis

    Un entorno de desarrollo integrado (IDE) de Microsoft, que proporciona un conjunto completo de herramientas que incluyen un editor de código, compilador, depurador y generador de perfiles (profiler), para varios lenguajes de programación y desarrollo multiplataforma. Una gran opción para principiantes, ya que su interfaz moderna es fácil de usar y requiere una personalización mínima de fábrica.


* :arrow_forward: **Qt Creator IDE**

    Sitio: https://www.qt.io/product/development-tools
    
    Precio: gratis para proyectos de código abierto (más detalles: [Qt Open Source](https://www.qt.io/download-open-source?hsCtaTracking=9f6a2170-a938-42df-a8e2-a9f0b1d6cdce%7C6cb0de4f-9bb5-4778-ab02-bfb62735f3e5))

    Inicialmente, Qt Creator se posicionó como un IDE para desarrollar interfaces gráficas para aplicaciones en C++. Con el tiempo, el marco ha adquirido numerosas capacidades y se ha convertido en un ecosistema integral para el desarrollo multiplataforma. Ofrece una vasta biblioteca de primitivas para diversas necesidades como redes, interfaz gráfica, trabajo con bases de datos y el manejo de formatos populares como imágenes y archivos de texto. Hoy en día, Qt Creator sirve como un competidor de Visual Studio y es particularmente popular entre los desarrolladores que crean aplicaciones para diversas distribuciones de Linux.


* :arrow_forward: **Xcode**

    Sitio: https://developer.apple.com/xcode/

    Precio: gratis

    El propio entorno de desarrollo de Apple y la única forma de crear aplicaciones para macOS e iOS. Viene con Clang y LLDB. Si trabajas en macOS, necesitarás Xcode al menos por sus herramientas de línea de comandos, incluso si prefieres escribir código en un editor diferente.


* :arrow_forward: **JetBrains CLion IDE**

    Sitio: https://www.jetbrains.com/clion

    Precio: gratis para uso no comercial (desde mayo de 2025); se requiere licencia paga para desarrollo comercial

    Potente IDE multiplataforma de JetBrains. Al igual que otros IDEs, proporciona un conjunto completo de herramientas para el desarrollo cómodo de software. Es conveniente para el desarrollo multiplataforma tanto en C como en C++.

## :flashlight: Extensiones

* :arrow_forward: **JetBrains ReSharper C++**

    Sitio: https://www.jetbrains.com/resharper-cpp

    Precio: gratis para estudiantes y profesores

    Una extensión para Microsoft Visual Studio, agrega funciones avanzadas para trabajar con el código fuente, como resaltado extendido de código y sugerencias, construcción de diagramas de dependencias entre proyectos, recomendaciones para corregir errores comunes en el código, información mejorada durante la depuración, búsqueda y navegación mejoradas dentro de proyectos, etc. Compite con Visual Assist.

* :arrow_forward: **Visual Assist**

    Sitio: https://www.wholetomato.com

    Una extensión para Microsoft Visual Studio que proporciona funciones adicionales para trabajar con el código fuente, como resaltado de código mejorado y sugerencias, mayor información durante la depuración y codificación, capacidades de búsqueda avanzadas y navegación de proyectos mejorada. Compite con JetBrains ReSharper.


* :arrow_forward: **Incredibuild**

    Sitio: https://www.incredibuild.com

    Precio: hay que contactar al equipo de incredibuild para saber el precio

    Aplicación/extensión para la compilación distribuida de proyectos, que une todas las estaciones de trabajo de los desarrolladores en una sola red, brindando la posibilidad de usar decenas de máquinas para ensamblar y compilar el código fuente. Esto acelera el proceso de construcción de grandes proyectos.

## :electric_plug: Gestores de paquetes y sistemas de compilación

* :arrow_forward: **CMake**

    Sitio: https://cmake.org

    Precio: gratis

    Un sistema de automatización multiplataforma para compilar una aplicación desde el código fuente, que genera los artefactos necesarios para el posterior ensamblaje en la plataforma de destino. Actualmente se considera la herramienta estándar para compilar varias bibliotecas cuando se suministran como fuente.

* :arrow_forward: **Conan**

    Sitio: https://conan.io

    Precio: gratis

    Un gestor de paquetes y dependencias para organizar bibliotecas y frameworks de C++. Soporta el trabajo en diversas plataformas como Windows y Linux, y tiene integración con herramientas como CMake y Visual Studio.

* :arrow_forward: **vcpkg**

    Sitio: https://vcpkg.io

    Precio: gratis

    Un gestor de paquetes gratuito y de código abierto para bibliotecas C y C++, desarrollado por Microsoft. Proporciona miles de bibliotecas listas para usar y se integra perfectamente con CMake y Visual Studio. Junto con Conan, es uno de los dos gestores de dependencias más populares en el ecosistema de C++.


* :arrow_forward: **Ninja**

    Sitio: https://ninja-build.org

    Precio: gratis

    Gestor de compilación de proyectos para aplicaciones C y C++. La principal ventaja de este gestor es el ensamblaje rápido del proyecto. Soporta el desarrollo multiplataforma y funciona con todos los compiladores populares.

* :arrow_forward: **ccache**

    Sitio: https://ccache.dev

    Precio: gratis

    Una caché de compilador: almacena los resultados de compilaciones anteriores y los reutiliza cuando vuelve a ocurrir la misma compilación, lo que puede acelerar drásticamente las reconstrucciones. Se sitúa de forma transparente frente a GCC o Clang y se integra con CMake en un par de líneas, convirtiéndolo en una de las victorias de tiempo de construcción más baratas en proyectos medianos y grandes.


## :mag: Analizadores de código y formateadores

* :arrow_forward: **clang-format**

    Sitio: https://clang.llvm.org/docs/ClangFormat.html

    Precio: gratis

    El formateador de código automático estándar de facto para C++. Un único archivo de configuración (`.clang-format`) almacenado en el repositorio mantiene consistente el estilo de código de todo el equipo y elimina los debates de formato en la revisión de código. Está soportado por defecto en casi todos los editores e IDEs.

* :arrow_forward: **clang-tidy**

    Sitio: https://clang.llvm.org/extra/clang-tidy/

    Precio: gratis

    Una herramienta de análisis estático (linter) del proyecto LLVM. Comprueba el código frente a cientos de reglas — patrones propensos a errores, problemas de rendimiento, legibilidad, estilo C++ moderno — y puede corregir automáticamente muchos de los problemas que encuentra. Está integrado en la mayoría de los IDEs, incluyendo Visual Studio, CLion, VS Code, y Qt Creator.

* :arrow_forward: **Sanitizers (ASan, UBSan, TSan)**

    Sitio: https://github.com/google/sanitizers

    Precio: gratis

    Herramientas de análisis dinámico integradas directamente en GCC, Clang y MSVC y habilitadas con banderas de compilador (p. ej., `-fsanitize=address`). AddressSanitizer detecta errores de memoria como el acceso fuera de los límites y el uso después de liberación (*use-after-free*), UndefinedBehaviorSanitizer detecta el comportamiento indefinido y ThreadSanitizer detecta las condiciones de carrera de datos. Ejecutar tus pruebas con sanitizadores habilitados se considera una práctica básica en el desarrollo moderno de C++.

* :arrow_forward: **Fuzzing (libFuzzer, AFL++)**

    Sitio: https://llvm.org/docs/LibFuzzer.html, https://github.com/AFLplusplus/AFLplusplus

    Precio: gratis

    El fuzzing es la alimentación automática de un flujo de datos aleatorios y deliberadamente malformados en tu código en busca de cuelgues (crashes) y bloqueos. Es especialmente útil para todo aquello que analiza (*parsea*) entrada externa: analizadores de formatos, protocolos de red, decodificadores. Por lo general, se ejecuta junto con sanitizadores: el fuzzer encuentra la entrada que desencadena un error y el sanitizador muestra exactamente dónde ocurrió. libFuzzer está integrado en Clang; AFL++ funciona como una herramienta independiente.

* :arrow_forward: **PVS Studio**

    Sitio: https://pvs-studio.com

    Precio: de pago; gratis para proyectos de código abierto y estudiantes

    Analizador de código estático multiplataforma (Windows, Linux, MacOS) por PVS-Studio. El objetivo principal del analizador es analizar el código fuente en busca de diversos errores que pueden pasar desapercibidos por los compiladores o durante la revisión del código. Ayuda a reducir el número de errores relacionados con la sintaxis del lenguaje y las trampas.


* :arrow_forward: **Cppcheck**

    Sitio: https://cppcheck.sourceforge.io

    Precio: gratis

    Un analizador de código gratuito que te ayuda a detectar errores comunes en tu código fuente que el compilador o la revisión de código podrían pasar por alto. Es multiplataforma y compatible con las distribuciones populares de Linux y Windows.


* :arrow_forward: **Valgrind**

    Sitio: https://valgrind.org

    Precio: gratis

    Un conjunto de herramientas que te pueden ayudar a investigar varios problemas mientras la aplicación se está ejecutando, como fugas de memoria y perfiles de rendimiento. Es compatible con múltiples distribuciones de Linux. En proyectos modernos, los sanitizadores cubren muchos de los mismos casos de uso con una sobrecarga mucho menor, pero Valgrind sigue siendo útil porque no requiere recompilación.

## :beetle: Depuradores

* :arrow_forward: **GDB (GNU Debugger)**

    Sitio: https://sourceware.org/gdb/

    Precio: gratis

    El depurador estándar en el mundo GNU/Linux. Te permite establecer puntos de interrupción, avanzar paso a paso por el código, inspeccionar variables y memoria, y analizar volcados de memoria (core dumps) de aplicaciones colgadas. La mayoría de los front-ends de depuración de IDE en Linux (VS Code, Qt Creator, CLion) utilizan GDB bajo el capó, por lo que comprender sus conceptos básicos da sus frutos incluso si en su mayoría depuras desde un IDE.

* :arrow_forward: **LLDB**

    Sitio: https://lldb.llvm.org

    Precio: gratis

    El depurador del proyecto LLVM y el depurador predeterminado en macOS (usado por Xcode). Ofrece capacidades similares a GDB con una arquitectura más moderna.

* :arrow_forward: **WinDbg**

    Sitio: https://learn.microsoft.com/windows-hardware/drivers/debugger/

    Precio: gratis

    El depurador de Microsoft para Windows. Para el trabajo diario en Windows, el depurador integrado en Visual Studio suele ser suficiente, pero WinDbg es indispensable cuando sus capacidades se quedan cortas: análisis de volcados de bloqueos (crash dumps) desde máquinas en producción, depuración de controladores y en modo kernel, trabajo con una aplicación sin código fuente. Una habilidad útil para cualquiera que desarrolle a bajo nivel o investigue bloqueos en las máquinas de los usuarios.

## :stopwatch: Analizadores de rendimiento (Profilers)

* :arrow_forward: **perf**

    Sitio: https://perfwiki.github.io/main/

    Precio: gratis

    El perfilador de muestreo estándar en Linux, integrado en el kernel. Muestra dónde pasa realmente su tiempo de CPU una aplicación, con detalles de contadores de hardware (errores de caché, malas predicciones de bifurcación) cuando los necesitas. A menudo se utiliza junto con visualizaciones *flame-graph* (gráficos de llama) para hacer evidentes los cuellos de botella (hotspots).

* :arrow_forward: **Tracy**

    Sitio: https://github.com/wolfpld/tracy

    Precio: gratis

    Un perfilador de cuadros (frames) en tiempo real que es especialmente popular en el desarrollo de juegos. Anotas zonas en tu código con macros ligeras y observas los tiempos en vivo en un cliente gráfico, hasta los marcos y subprocesos (threads) individuales. Multiplataforma y con una sobrecarga notablemente baja.

* :arrow_forward: **Intel VTune Profiler**

    Sitio: https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html

    Precio: gratis

    Un perfilador potente para el análisis de rendimiento profundo en x86: puntos calientes (hotspots), eficiencia de subprocesos, patrones de acceso a la memoria y métricas a nivel de microarquitectura. La herramienta de referencia cuando el resultado de `perf` no es lo suficientemente detallado. En Windows, el IDE de Visual Studio también incluye un potente perfilador de CPU y memoria integrado.

## :white_check_mark: Pruebas (Testing) y benchmarks

* :arrow_forward: **GoogleTest (gtest/gmock)**

    Sitio: https://github.com/google/googletest

    Precio: gratis

    El framework de pruebas unitarias más utilizado en C++. Viene con GoogleMock para crear stubs y mocks, lo que te permite probar el código de forma aislada de sus dependencias — bases de datos, red, sistema de archivos. Se integra bien con CMake y se puede incluir mediante cualquiera de los gestores de paquetes populares.

* :arrow_forward: **Catch2**

    Sitio: https://github.com/catchorg/Catch2

    Precio: gratis

    Una alternativa más ligera a GoogleTest con una sintaxis concisa. Una prueba aquí es una función ordinaria con una macro `REQUIRE` en lugar de un conjunto de macros de comparación especiales. Una buena opción para proyectos pequeños y para familiarizarse con las pruebas unitarias: puede ser incluido como un único archivo de cabecera (header).

* :arrow_forward: **Google Benchmark**

    Sitio: https://github.com/google/benchmark

    Precio: gratis

    Una biblioteca para microbenchmarks. Escoge la cantidad de repeticiones por sí misma para que el resultado sea estadísticamente significativo, y puede combatir la tendencia del optimizador de descartar código cuyo resultado nunca se usa. Es necesaria cuando tienes que comparar dos implementaciones por velocidad: medir el tiempo "a mano" con la lectura del reloj antes y después casi siempre da un resultado poco fiable.

## :robot: Herramientas de IA

Los asistentes de IA se han convertido en parte del conjunto de herramientas diario de un desarrollador: aceleran la escritura de código repetitivo (boilerplate), te ayudan a orientarte en una base de código desconocida y explican errores del compilador. Al mismo tiempo, no reemplazan el conocimiento del lenguaje — las razones se explican a continuación.

* :arrow_forward: **GitHub Copilot**

    Sitio: https://github.com/features/copilot

    Precio: hay un nivel gratuito limitado; el acceso completo es de pago, y gratuito para estudiantes, profesores y mantenedores de proyectos populares de código abierto

    Autocompletado de código directamente en el editor: sugiere las siguientes líneas en función del contexto del archivo y el proyecto. Se integra con Visual Studio, VS Code, CLion, y otros IDEs populares.

* :arrow_forward: **Claude Code**

    Sitio: https://claude.com/product/claude-code

    Precio: de pago, como parte de una suscripción

    Un asistente que trabaja en la terminal y en el IDE: lee todo el proyecto, realiza ediciones en varios archivos a la vez, y ejecuta la compilación y las pruebas. Está dirigido a tareas más grandes que una sola línea — refactorización, exploración de código desconocido, redacción de pruebas.

* :arrow_forward: **Cursor**

    Sitio: https://cursor.com

    Precio: hay un nivel gratuito; las funciones avanzadas son de pago

    Un editor basado en VS Code con un asistente de IA incorporado. Puede responder preguntas sobre el código fuente y hacer ediciones en varios archivos a la vez, manteniendo las extensiones y configuraciones familiares de VS Code.

* :arrow_forward: **Modelos locales (Ollama, llama.cpp)**

    Sitio: https://ollama.com, https://github.com/ggml-org/llama.cpp

    Precio: gratis

    Ejecutar modelos en tu propia máquina. Son inferiores en calidad a los modelos en la nube y requieren recursos notables, pero el código nunca sale de tu computadora. Esta es una opción para proyectos donde el envío de código fuente a servicios externos está prohibido. Por cierto, `llama.cpp` es en sí mismo un ejemplo instructivo de un proyecto moderno en C++.

### :warning: Qué tener en cuenta

- **Verifica todo lo que se genera.** Un modelo puede producir código plausible pero incorrecto: funciones de la biblioteca estándar que no existen, errores sutiles sobre el tiempo de vida de los objetos (object-lifetime bugs), condiciones de carrera. En C++ el costo de tal error es alto — el comportamiento indefinido puede no aparecer en ninguna prueba y puede explotar en la máquina de un usuario. Esta es exactamente la razón por la que el conocimiento del lenguaje sigue siendo obligatorio: para verificar una respuesta, necesitas comprender el tema no peor de lo que lo harías al escribir el código a mano.
- **Sigue la política de la empresa.** En muchas organizaciones, el envío de código de trabajo a servicios externos está restringido o prohibido. Aclara las reglas antes de conectar un asistente, no después.
- **Recuerda las licencias.** El código generado puede reproducir fragmentos de proyectos de otras personas junto con sus obligaciones de licencia. Para proyectos comerciales esto es un riesgo aparte que vale la pena discutir con tu equipo.
- **No te saltes la etapa de aprendizaje.** Un asistente te libera de la rutina, pero si resuelve por ti los mismos problemas de los que se supone que debes aprender, no crecerás como ingeniero. Al principio de tu carrera, es útil resolver un problema tú mismo primero y solo entonces compararlo con lo que sugiere el modelo.

## :floppy_disk: Clientes de Git

* :arrow_forward: **SmartGit**

    Sitio: https://www.syntevo.com/smartgit/

    Precio: gratis para proyectos de código abierto

    Una herramienta completa y multiplataforma para trabajar con repositorios de Git. Viene con las siguientes características: recibir y enviar cambios al repositorio, ver el historial de cambios, un editor de texto para resolver conflictos, etc. Soporta la integración con todos los repositorios populares como GitHub, BitBucket, GitLab, etc.

* :arrow_forward: **Atlassian SourceTree**

    Sitio: https://www.sourcetreeapp.com/

    Precio: gratis

    Una gran alternativa gratuita para trabajar con Git usando una GUI (interfaz gráfica de usuario). Tiene la misma funcionalidad que SmartGit, con la excepción de que no cuenta con su propio editor para la resolución de conflictos. Sin embargo, esto puede ser arreglado fácilmente integrando Visual Studio Code o cualquier otro editor que pueda comparar archivos. Ten en cuenta que a diferencia de SmartGit, solo está disponible para Windows y macOS. Es compatible con la integración con repositorios populares como GitHub, BitBucket, GitLab, etc.


* :arrow_forward: **Git Kraken**

    Sitio: https://www.gitkraken.com/

    Precio: gratis para proyectos de código abierto

    Un cliente multiplataforma y muy eficiente para Windows, Linux y MacOS. Admite la integración con GitHub, Bitbucket y Gitlab, y tiene todas las funciones necesarias para el trabajo diario, como ver el historial de cambios, enviar y recibir cambios, cambiar entre ramas y un editor de resolución de conflictos incorporado.

---

[**A la página principal**](../README.md)
