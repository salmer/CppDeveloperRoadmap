# :robot: El desarrollador de C++ y la inteligencia artificial

Con la llegada de modelos que escriben código con confianza, muchos aspirantes a desarrolladores se han hecho una pregunta razonable: ¿siquiera vale la pena ingresar a la profesión? Es una pregunta justa, y descartarla con un "nah, todo será igual que antes" sería incorrecto. Veamos qué está pasando realmente.

La respuesta corta: los ingenieros siguen siendo necesarios, pero el estándar ha cambiado. He aquí por qué.

## :dna: La IA reproduce aquello con lo que fue entrenada

Un modelo se entrena en un vasto cuerpo de código ya escrito y, por su propia naturaleza, produce lo que apareció con mayor frecuencia en esos datos. Hace un trabajo excelente con tareas que la humanidad ya ha resuelto miles de veces: analizar JSON, levantar un servidor HTTP, escribir pruebas para una función fácil de entender.

Sus limitaciones crecen exactamente de la misma raíz:

- **Lo inusual se maneja mal.** Tu dominio del problema, tus limitaciones de hardware, la compensación (trade-off) entre memoria y latencia en tu caso particular: nada de eso estaba en los datos de entrenamiento. Y el trabajo de ingeniería consiste en gran parte en estas situaciones de "pero en nuestro caso todo es diferente".
- **Un sesgo hacia el código antiguo.** El C++ de código abierto (open-source) se ha acumulado durante décadas y está escrito predominantemente en un estilo antiguo. Por lo tanto, los modelos te entregan felizmente `new`/`delete` en lugar de punteros inteligentes, bucles crudos en lugar de algoritmos, cadenas de C (C-strings) en lugar de `std::string_view`. El código funcionará, pero no será el código que querrás ver en tu proyecto.
- **Confianza no es corrección.** Un modelo puede citar una función de la biblioteca estándar inexistente o confundir el comportamiento de una sobrecarga, y lo afirmará exactamente en el mismo tono que una respuesta correcta.

## :warning: Por qué el costo de un error es mayor en C++

En los lenguajes con memoria administrada, el código incorrecto generalmente falla de forma ruidosa e inmediata. En C++ este no es el caso.

- **El comportamiento indefinido puede no aparecer en las pruebas.** Una condición de carrera (data race), el acceso a memoria liberada, un acceso a un arreglo fuera de los límites: todo esto puede funcionar "bien" en tu máquina durante años y luego explotar en la máquina de un usuario o después de una actualización del compilador. Ninguna prueba garantiza que el código generado esté libre de ellos.
- **El tiempo de vida de un objeto es el punto más complicado.** Aquí es exactamente donde los modelos se equivocan más a menudo: devuelven una referencia a un objeto local, capturan una variable en una lambda por referencia y no se detienen a pensar quién es el propietario del objeto.
- **Concurrencia.** El código que parece correcto puede contener una condición de carrera que se reproduce una vez a la semana bajo carga.

La conclusión es simple: **solo puedes aceptar código que seas capaz de verificar**. Y para verificar el código en C++, necesitas saber C++ no menos que cuando lo escribes a mano. Las herramientas que ayudan (sanitizers, static analyzers, fuzzing) se describen en [Conjunto de herramientas del lenguaje](../English/Tooling.md).

## :bulb: El cuello de botella del desarrollo no es la velocidad de escritura

Este es el punto más importante. El trabajo de un ingeniero nunca se ha reducido a escribir caracteres. Consiste en:

- descubrir qué es lo que realmente necesita el cliente (por lo general, tampoco lo entienden bien a la primera);
- decidir qué errores en el sistema **no deben** ocurrir y qué hacer cuando ocurren de todos modos;
- compensaciones (trade-offs): velocidad versus legibilidad, plazos versus deuda técnica, confiabilidad versus costo;
- ser responsable del resultado.

Ninguna de estas tareas puede delegarse a un modelo, no porque "no sea lo suficientemente inteligente", sino porque son preguntas sobre personas, dinero y responsabilidad. Si una aplicación perjudica a un usuario, es la empresa y los ingenieros específicos quienes responden por ella, no la herramienta. En campos donde el software está certificado —medicina, aviónica, automotriz (ver [Estándares de codificación y requisitos normativos](Compliance.md))— esto ya no es filosofía, sino un requisito literal: un humano firma el resultado.

Otra observación, conocida mucho antes de las redes neuronales: **leer el código de otra persona es más difícil que escribir el tuyo propio**. A medida que hay más código y se escribe más rápido, el cuello de botella ya no es escribir, sino comprender y revisar. Ese es un trabajo para un ingeniero, y es más probable que su volumen crezca.

## :chart_with_upwards_trend: Qué cambia realmente

Sería deshonesto decir que no está pasando nada. Algo está pasando, y esto es lo que ya es visible:

- **La rutina pierde su valor.** La capacidad de escribir rápidamente otra clase repetitiva (boilerplate) ya no es una ventaja en sí misma.
- **Crece el valor de la verificación y el pensamiento sistémico.** La capacidad de notar que una solución propuesta es elegante pero no se mantendrá bajo carga o no encajará en la arquitectura existente se convierte en una habilidad clave.
- **El nivel de entrada ha subido.** Siempre se esperaba que un desarrollador junior pudiera escribir código. Ahora se espera cada vez más que también puedan evaluar el código de otra persona, incluido el código escrito por una máquina.

La conclusión práctica: invierte en los fundamentos (el modelo de memoria, el tiempo de vida de los objetos, la concurrencia, la arquitectura, la depuración). Todo lo que te permita juzgar si una solución es correcta. De eso se trata exactamente el [roadmap](README.md).

## :hourglass: Una trampa para los que aún están aprendiendo

El riesgo más grave de la IA para un desarrollador principiante no es "te quitará tu trabajo", sino que se interpondrá **en el camino del aprendizaje**.

La habilidad surge de luchar con un problema: lo intentas, fallas, descubres por qué y un modelo mental de lo que está sucediendo permanece en tu cabeza. Si le preguntas a un asistente en cada dificultad, el problema se resuelve pero el modelo mental no. Después de un año de práctica como esa, resulta que no tienes forma de comprobar la respuesta del asistente.

Qué hacer al respecto:

- En los ejercicios de aprendizaje, **resuélvelo tú mismo primero**, y acude al asistente para una revisión de una solución terminada: "qué se podría haber hecho mejor aquí y por qué".
- Pide una explicación, no código: por qué de esta manera, cuáles son las alternativas, qué se rompe cuando cambian las condiciones.
- No pegues código que no puedas explicar línea por línea. Esta regla funciona igual de bien para el código de Stack Overflow y para el código de un modelo.
- De vez en cuando, escribe algo sin asistente en absoluto, para que puedas ver honestamente tu nivel real.

## :handshake: Cómo usarlo de manera útil

- **Como acelerador de rutina:** código repetitivo (boilerplate), estructura de pruebas, exploración de una API desconocida, borradores de documentación.
- **Como compañero de explicaciones:** "¿por qué el compilador se queja así?" — los modelos decodifican los errores de las plantillas (templates) de C++ notablemente mejor que el compilador.
- **Como navegador a través de una base de código desconocida:** comprender rápidamente dónde están las cosas y cómo se conectan.
- **Como revisor:** pídele que encuentre problemas en tu código. No como la última palabra, sino como un par de ojos más.

Y tres reglas que vale la pena tener en cuenta en todo momento: verifica lo que se genera, sigue la política de tu empresa sobre el envío de código a servicios externos y recuerda los riesgos de las licencias. Más sobre esto en la sección de [herramientas de IA](../English/Tooling.md).

## :telescope: Lo que nadie sabe

Sinceramente: nadie sabe cómo será la profesión en diez años, ni los autores de este roadmap, ni los propios autores de los modelos. Cualquiera que prediga con confianza que "todos serán reemplazados" o "nada cambiará" está haciendo pasar una ilusión por un hecho.

Lo que se puede decir con confianza: la demanda de personas que entiendan cómo funcionan los sistemas y puedan ser responsables del resultado no ha desaparecido hasta ahora. Las herramientas de desarrollo siempre han cambiado: ensamblador, compiladores, IDEs, autocompletado, búsqueda en internet. Cada vez el estribillo era "ahora cualquiera puede programar", y cada vez había más trabajo, no menos, porque el desarrollo más barato abría nuevos problemas por resolver. El giro actual aún puede resultar diferente, pero hasta ahora no hay base para apostar que el conocimiento profundo perderá su valor repentinamente.

---

[**A la página principal**](README.md)
