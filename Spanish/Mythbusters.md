# :ghost: Mitos y Leyendas de C++

## :question: C++ está muerto, es imposible programar algo con él

C++ no está muerto.

De hecho, se ha mantenido consistentemente entre los lenguajes de programación principales en varias clasificaciones, como el índice [Tiobe](https://www.tiobe.com/tiobe-index/). La percepción de que C++ es un "lenguaje muerto" surgió a principios de los años 2000, cuando el comité de estandarización del lenguaje estaba inactivo. Sin embargo, C++ ha experimentado un resurgimiento desde entonces, añadiéndose nuevas características y funcionalidades cada tres años desde el estándar C++11. A pesar de esto, todavía hay quienes perpetúan los mitos y leyendas de que C++ es un lenguaje difícil y problemático, a menudo porque no se han mantenido al día con los desarrollos del lenguaje o solo han tenido una exposición limitada a él en su educación.

## :question: Los programadores de verdad aprenden C++ usando Linux/Vim/gcc

Si no estás familiarizado con la combinación mencionada, se recomienda centrarse en aprender los fundamentos de C++ primero. Se sugiere comenzar a desarrollar tus primeras aplicaciones utilizando el IDE Microsoft Visual Studio. Para más información, consulta los [Libros PreJunior](../English/Books/PreJunior.md).

Tomar el camino desafiante puede parecer genial, pero hay una alta probabilidad de que la cantidad de información necesaria para crear un programa "Hello World" usando Linux, Vim y GCC sea abrumadora. Esto podría llevar a una frustración temprana y a la desilusión con la programación en general. Intenta seguir un camino que comience con cosas simples y aumente gradualmente en complejidad. Al igual que un novato no debería intentar levantar los pesos más pesados durante su primer entrenamiento, la misma regla se aplica al aprendizaje. Una vez que te sientas cómodo con el lenguaje, puedes intentar desarrollar usando Linux. Pero esa es otra historia completamente distinta...

## :question: Es mejor dominar C/Ensamblador/etc. antes de aprender C++

¡No, no y no de nuevo!

Esta afirmación persiste debido a dos escenarios generalizados: es cómo se enseñaba C++ en las universidades en el pasado, y los miembros de la "Vieja Guardia" pasaron por un camino similar. El C++ moderno no requiere un enfoque tan desafiante. El lenguaje es autosuficiente y se puede aprender sin ninguna base previa. Es más probable que aprender C++ a través del enfoque "C -> C++" resulte en confusión y en un deseo de escribir C++ en un estilo de "C con clases".

## :question: Aprende C++ usando el libro de Stroustrup

Una afirmación muy perjudicial que proviene de la "Vieja Guardia" o de aquellos que nacieron con un teclado en la mano.

Este consejo probablemente lo den aquellos que tienen amplia experiencia en el desarrollo de otros lenguajes (como C, Fortran, Delphi, etc.) y luego hicieron la transición a C++. Stroustrup escribió el libro [The C++ Programming Language](https://www.amazon.com/C-Programming-Language-4th/dp/0321563840) como una referencia, por lo que debe usarse de manera adecuada, lo cual requiere cierto conocimiento del lenguaje. En cambio, es mejor consultar la sección de [Libros](../English/Books/Overview.md), donde encontrarás libros para todos los niveles de dominio del lenguaje.

## :question: Aprende C++ usando solo el Estándar

Otra afirmación esnob.

El estándar moderno de C++, que supera las 2000 páginas, requiere pago para acceder a la versión actualizada y no está compuesto de manera fácil de usar. Si bien es elogiable para aquellos que aprendieron el lenguaje usando su estándar, no se recomienda como una forma de aprender para la mayoría de las personas. En cambio, es mejor revisar la sección de [Libros](../English/Books/Overview.md), donde encontrarás libros adecuados para varios niveles de dominio del lenguaje.

## :question: El Comportamiento Indefinido (Undefined Behavior) acecha al desarrollador en todas partes

Más probablemente no que sí.

El C++ moderno y las herramientas que han surgido alrededor del lenguaje permiten evitar la gran mayoría de los problemas relacionados con el comportamiento indefinido (Undefined Behavior). Podemos dar un consejo sencillo: cuando no estés seguro de lo que hace una construcción en particular, lee sobre ella en [CppReference](https://en.cppreference.com), [StackOverflow](https://stackoverflow.com/) u otros recursos dedicados. Si aún tienes dudas después de leer, intenta reescribir el código de una manera más sencilla para evitar el comportamiento indefinido. Hay un gran poder en la simplicidad.

## :question: Uno necesita gestionar la memoria manualmente, no hay recolección de basura (garbage collection) en el lenguaje

Esta es otra leyenda urbana de la "Vieja Guardia", que dejó de escribir C++ antes de C++11 o de aquellos que lo aprendieron superficialmente en la universidad y pasaron por alto los estándares más recientes. El C++ moderno tiene un conjunto de primitivas en su biblioteca estándar que son responsables de la asignación y desasignación automática de memoria. La gestión manual de memoria ha quedado en el camino. Muchos equipos y empresas incluso tienen la regla: "Cero punteros crudos" (No raw pointers). Una vez más, no descuides las herramientas modernas y los sanitizers, ya que pueden detectar posibles fugas de memoria a nivel de código fuente.

## :question: C++ es solo para áreas heredadas (legacy)

Parcialmente es cierto, pero vale la pena señalar que no solo es aplicable a C++. La calidad del código en cualquier lenguaje depende principalmente de la cultura técnica de un equipo y sus pioneros, no solo del lenguaje. La mayor parte del código heredado se produce debido a factores humanos: el nivel de habilidad del desarrollador, su ética de trabajo y estimaciones incorrectas, entre otros. Hoy en día, hay muchos proyectos escritos en C++ que han estado funcionando 24/7 durante años y son la base de los ingresos de una empresa. En tales casos, es peligroso realizar cambios significativos en un corto período. Los desarrolladores tienen mucho cuidado al hacer cambios para evitar regresiones. Sin embargo, no pienses que trabajar en proyectos heredados no puede ayudarte a mejorar. De hecho, estos proyectos pueden proporcionar un desafío que puede brindarte una gran experiencia en áreas como lectura de código, ingeniería inversa, pruebas, diseño de arquitectura de software, automatización y recopilación de requisitos, entre otras.

---

[**A la página principal**](README.md)
