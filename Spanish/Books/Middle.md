# :sunglasses: Middle

## :pencil: C++

- [Scott Meyers - Effective Modern C++: 42 Specific Ways to Improve Your Use of C++11 and C++14](https://www.amazon.com/Effective-Modern-Specific-Ways-Improve/dp/1491903996)

    Es un nuevo capítulo en la colección de libros de Scott Meyers. Este libro recopila un conjunto de consejos para los estándares C++11/14.

- Nicolai Josuttis:
    - [C++17 - The Complete Guide](https://leanpub.com/cpp17)
    - [C++20 - The Complete Guide](https://leanpub.com/cpp20)

    El libro de Meyers se detiene en C++14, y estos dos volúmenes continúan donde él lo dejó. Cada uno repasa sistemáticamente todo lo que añadió su estándar (tanto características del lenguaje como de la biblioteca) con ejemplos prácticos y consejos sobre cuándo (y cuándo no) usar las nuevas herramientas.

- [Nicolai Josuttis - C++ Move Semantics: The Complete Guide](https://leanpub.com/cppmove)

    La semántica de movimiento (move semantics) es uno de esos temas que "parecen claros" hasta que comienzas a profundizar en los detalles: cuándo el compilador aplica un movimiento por su cuenta, en qué se diferencia `std::move` de `std::forward`, por qué a veces un movimiento se convierte silenciosamente en una copia, y cómo se relaciona la regla de los cinco (rule of five) con `noexcept`. El libro analiza todo esto paso a paso y con ejemplos. Es uno de los temas más frecuentes en las entrevistas de nivel Middle.

- [Klaus Iglberger - C++ Software Design: Design Principles and Patterns for High-Quality Software](https://www.amazon.com/Software-Design-Principles-Patterns-High-Quality/dp/1098113160)

    Una versión moderna de los patrones de diseño, escrita específicamente para C++. Muestra cómo se ven los patrones clásicos cuando se construyen sobre los modismos (idioms) actuales (semántica de valor, borrado de tipos, `std::variant`) en lugar de profundas jerarquías de herencia, y es un gran puente entre conocer el lenguaje y diseñar con él.

- [Anthony Williams - C++ Concurrency in Action](https://www.amazon.com/C-Concurrency-Action-Anthony-Williams/dp/1617294691/ref=sr_1_3?keywords=C%2B%2B+Concurrency+in+Action%3A+Practical+Multithreading&qid=1636314477&s=books&sr=1-3)

    Este libro es una guía completa sobre la programación multihilo y el uso de las características de la biblioteca estándar. Proporciona explicaciones detalladas sobre todas las primitivas y sus complejidades "detrás de escena".

- Herb Sutter:
    - [Exceptional C++: 47 Engineering Puzzles, Programming Problems, and Solutions](https://www.amazon.com/Exceptional-Engineering-Programming-Problems-Solutions/dp/0201615622)
    - [Exceptional C++ Style: 40 New Engineering Puzzles, Programming Problems, and Solutions](https://www.amazon.com/Exceptional-Style-Engineering-Programming-Solutions/dp/0201760428) 
    - [More Exceptional C++: 40 New Engineering Puzzles, Programming Problems, and Solutions](https://www.amazon.com/More-Exceptional-Engineering-Programming-Solutions/dp/020170434X)

    La colección de libros cubre muchas tareas relacionadas con el diseño o la escritura de código en C++, ofreciendo una variedad de soluciones efectivas. Muchas de estas soluciones se han considerado modismos clásicos y se utilizan ampliamente en diversos proyectos.

- [David Vandevoorde - C++ Templates: The Complete Guide](https://www.amazon.com/C-Templates-Complete-Guide-2nd/dp/0321714121)

    El libro más nuevo y relevante sobre la metaprogramación en C++, específicamente sobre plantillas (templates), es un trabajo completo que describe las técnicas y fundamentos relevantes añadidos en los estándares recientes, incluido C++17. Si busca escribir código genérico y parametrizado, este libro se convertirá en un recurso indispensable para usted, ofreciendo conocimientos sobre los conceptos básicos de las plantillas así como sobre una multitud de matices relacionados con diferentes técnicas.


## :bicyclist: Optimización para aplicaciones C++

- [Kurt Guntheroth - Optimized C++: Proven Techniques for Heightened Performance](https://www.amazon.com/Optimized-Proven-Techniques-Heightened-Performance/dp/1491922060)

    Este libro es una guía para mejorar el rendimiento de las aplicaciones en C++. Algunos de los consejos de este libro se basan en varios modismos y trucos descritos en los libros de Herb Sutter o Scott Meyers. Se recomienda leer este libro después de leer los libros mencionados anteriormente.

- [Agner Fog - Optimizing software in C++](https://agner.org/optimize/optimizing_cpp.pdf) o [Optimization manuals](https://agner.org/optimize) 

    Las guías de orientación práctica proporcionan información completa sobre las posibilidades de optimización potenciales para aplicaciones desarrolladas en C++ o relacionadas con la interacción con la CPU, la memoria, etc.

## :electric_plug: Habilidades duras (Hard skills)

- [Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides or "Gang of Four" - Design Patterns: Elements of Reusable Object-Oriented Software](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)

    Este libro es una guía clásica sobre patrones de diseño. Cada patrón se describe detalladamente y se aconseja sobre su caso de uso apropiado. Este libro es una buena continuación de "Head First Design Patterns" de Eric Freeman. Sin embargo, esté preparado, ya que este libro es más complejo que el anterior.

- [Gary McLean Hall - Adaptive Code](https://www.amazon.com/Adaptive-Code-Developer-Best-Practices/dp/0136891446)
    
    Este libro es un excelente recurso para comprender los principios SOLID del diseño de software. Las explicaciones se presentan de forma sencilla, haciéndolas fáciles de entender. Los ejemplos de código, que están escritos en C#, también son sencillos y sirven para ilustrar los principios con eficacia.

- [Robert Martin - Clean Architecture: A Craftsman's Guide to Software Structure and Design](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
 
    Este libro, escrito por el Tío Bob (Uncle Bob), proporciona orientación sobre cómo abordar el diseño de software con un enfoque en la arquitectura. Enfatiza la importancia de pensar en la arquitectura de una aplicación o componente antes de comenzar a codificar. El libro ofrece conocimientos sobre qué considerar al analizar el diseño de una solución y ayuda a prevenir errores comunes en el diseño de software. Este libro es un gran punto de partida para las personas interesadas en tareas arquitectónicas en el diseño de software que buscan obtener una comprensión más profunda del campo. El conocimiento contenido en este libro es ampliamente utilizado entre ingenieros y les ayudará a evitar errores generalizados.

- [Samary Baranov - Finite State Machines and Algorithmic State Machines: Fast and Simple Design of Complex Finite State Machines](https://www.amazon.com/Finite-State-Machines-Algorithmic-Complex-ebook/dp/B078RYYBCJ)

    Esta es una guía breve y práctica sobre cómo abordar la programación utilizando la teoría de máquinas de estado finito. No encontrará una explicación más simple y elegante de la teoría de máquinas finitas y sus aplicaciones prácticas.

- [Vladimir Khorikov - Unit Testing Principles, Practices, and Patterns: Effective testing styles, patterns, and reliable automation for unit testing, mocking, and integration testing with examples in C#](https://www.amazon.com/Unit-Testing-Principles-Practices-Patterns-ebook/dp/B09782L692)

    El libro proporciona información sobre las mejores prácticas y los antipatrones comunes que rodean el tema de las pruebas unitarias (unit testing). Después de leer este libro, armado con sus nuevas habilidades, tendrá el conocimiento necesario para convertirse en un experto en la entrega de proyectos exitosos que son fáciles de mantener y extender, gracias a las pruebas que construya en el camino.


## :zap: Sistemas operativos

- [Andrew S. Tanenbaum - Modern Operating Systems](https://www.amazon.com/Modern-Operating-Systems-Andrew-Tanenbaum/dp/013359162X)

    Esta es una guía completa de los sistemas operativos, que cubre su construcción y diversos aspectos como los sistemas de archivos, redes, gestión de memoria, programación de tareas y multihilo. El libro proporciona explicaciones detalladas en términos simples, sin centrarse en una distribución de SO específica. Cada capítulo ofrece una exploración detallada de diferentes aspectos de los sistemas operativos, convirtiéndolo en un recurso fundamental para comprender este tema complejo.

- [Mark Russinovich - Windows Internals, Part 1](https://www.amazon.com/Windows-Internals-Part-architecture-management/dp/0735684189), [Mark Russinovich - Windows Internals, Part 2](https://www.amazon.com/Windows-Internals-Part-2-7th/dp/0135462401)

    Este libro profundiza en los mismos temas que el libro anterior, pero centrándose exclusivamente en el sistema operativo Microsoft Windows. Proporciona una mirada profunda y detallada a cada aspecto del SO con un enfoque específico en Windows y cubre varios matices y aspectos que pueden no ser declarados oficialmente por los desarrolladores. Es un recurso útil para aquellos que desarrollan aplicaciones de bajo nivel que requieren una interacción intensiva con las bibliotecas del sistema del SO.

- [Christopher Negus - Linux Bible](https://www.amazon.com/Linux-Bible-Christopher-Negus/dp/1394317468)

    Este libro puede servir como continuación del trabajo de Tanenbaum, profundizando en las complejidades del sistema operativo Linux. El libro incluye un análisis detallado de varios aspectos del SO, centrándose en distribuciones populares como Red Hat, Ubuntu y Fedora. Es un recurso ideal para los desarrolladores que utilizan Linux a diario.

- [Ulrich Drepper - What Every Programmer Should Know About Memory](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf)

    Este artículo proporciona una descripción general completa de cómo funciona la memoria de la PC y por qué opera de la manera descrita. Presenta no solo información de alto nivel, sino que también profundiza en aspectos de bajo nivel, lo que lo hace ideal para aquellos que desean profundizar en el tema.


## :globe_with_meridians: Redes de computadoras

- [Andrew S. Tanenbaum - Computer Networks](https://www.amazon.com/Computer-Networks-Andrew-Tanenbaum/dp/0136764053)

    Un libro clásico sobre los fundamentos teóricos de las redes de computadoras que proporciona una descripción detallada, comenzando desde la capa física hasta los protocolos de transferencia de datos. Será extremadamente útil para los desarrolladores que están muy involucrados en proyectos que interactúan con redes.

- [Victor Olifer - Computer Networks: Principles, Technologies and Protocols for Network Design](https://www.amazon.com/Computer-Networks-Principles-Technologies-Protocols-ebook/dp/B001GQ35P4)

    Este libro proporciona información completa sobre los conceptos básicos de las redes informáticas. Puede presentar la información de una manera un poco más compleja en comparación con el trabajo de Tanenbaum. Como resultado, se recomienda elegir el libro que presente la información en un estilo que sea más adecuado para usted.

---

[**Volver**](Overview.md) | [**Ir a la página principal**](../README.md)
