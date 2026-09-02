# :balance_scale: Estándares de codificación y requisitos normativos

C++ ha ocupado tradicionalmente las áreas donde el costo de un error no se mide en dinero perdido sino en vidas humanas: electrónica automotriz, dispositivos médicos, aviónica, automatización industrial, transporte ferroviario. En tales proyectos, la libertad del lenguaje se convierte en un problema, por lo que se restringe, con un conjunto de reglas de codificación, comprobaciones obligatorias y un proceso de desarrollo documentado.

Este artículo es un mapa general del territorio, no una guía de certificación. Su objetivo es que comprendas a qué se refiere cuando una oferta de trabajo dice "experiencia en MISRA" o "proyectos ISO 26262", y que sepas dónde buscar los detalles.

Hay una gran cantidad de estándares y requisitos, y a continuación solo se recopilan los más destacados. No existe un "conjunto obligatorio" único: cada proyecto utiliza su propio subconjunto según la industria, el país, el cliente y la clase de criticidad. Tiene sentido profundizar en un estándar específico cuando te lo encuentras realmente en tu proyecto, no solo por si acaso.

> :warning: Los requisitos y los plazos cambian. Antes de tomar decisiones, verifica con las ediciones actuales de los estándares y con los abogados de tu empresa: este artículo es para orientación, no para conclusiones legales.

## :straight_ruler: Estándares de codificación

Restringen el lenguaje a un subconjunto con menos formas de dispararte en el pie: sin asignación dinámica de memoria después de la inicialización, sin excepciones, sin conversiones de tipos implícitas, etc. El cumplimiento es verificado por analizadores estáticos; tales conjuntos de reglas no se verifican a mano.

* :arrow_forward: **MISRA C++:2023** - [misra.org.uk](https://misra.org.uk)

    El conjunto de reglas más conocido para C++ en sistemas críticos para la seguridad. Reemplazó a MISRA C++:2008 y cubre C++17. Un cambio importante: absorbió las pautas de **AUTOSAR C++14**, por lo que en lugar de dos conjuntos de reglas que compiten, como antes, ahora hay uno solo avanzando. Si te encuentras con un proyecto en AUTOSAR C++14, esa es la generación anterior del mismo enfoque ([autosar.org](https://www.autosar.org)).

* :arrow_forward: **SEI CERT C++** - [wiki.sei.cmu.edu](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046682)

    Un conjunto de reglas con énfasis en la seguridad (security): cómo evitar construcciones que conducen a vulnerabilidades. A diferencia de MISRA, está disponible de forma gratuita y abierta: una buena manera de familiarizarse con el género en sí, incluso si tu proyecto no está siendo certificado.

* :arrow_forward: **C++ Core Guidelines** - [isocpp.github.io](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

    Pautas de Bjarne Stroustrup y Herb Sutter. A diferencia de MISRA, no restringen el lenguaje, sino que te empujan hacia un estilo moderno. Formalmente no son un documento regulatorio, pero son útiles para cualquier desarrollador de C++; se pueden verificar parcialmente a través de `clang-tidy` y la [Microsoft GSL](https://github.com/microsoft/GSL).

## :shield: Seguridad funcional

Éstos responden a la pregunta "qué debe suceder para que el sistema no haga daño en caso de un fallo". Regulan no tanto el código como el proceso: requisitos, trazabilidad, pruebas, documentación y calificación de las herramientas utilizadas.

El estándar base en esta área es **IEC 61508**, que introduce los Niveles de Integridad de Seguridad (Safety Integrity Levels) SIL 1-4. Los estándares de la industria a continuación son sus adaptaciones:

* :arrow_forward: **ISO 26262** - automotriz - [iso.org](https://www.iso.org/standard/68383.html)

    Seguridad funcional de vehículos de carretera. Introduce los niveles ASIL de la A a la D, donde D es el más estricto (por ejemplo, control de frenos o dirección). Aquí es donde el emparejamiento "ISO 26262 + MISRA C++" se encuentra más a menudo.

* :arrow_forward: **IEC 62304** - software médico - [iso.org](https://www.iso.org/standard/38421.html)

    El ciclo de vida del software para dispositivos médicos. Define las clases de seguridad A, B y C dependiendo de si un fallo puede provocar daños a la salud y qué tan grave. El cumplimiento de este estándar es la forma principal de demostrar la conformidad con el Reglamento Europeo de Dispositivos Médicos **MDR** ([Reglamento (UE) 2017/745](https://eur-lex.europa.eu/eli/reg/2017/745/oj)), así como con los requisitos de la FDA en los EE. UU.

* :arrow_forward: **DO-178C** - aviónica - [rtca.org](https://www.rtca.org)

    Requisitos para software aerotransportado. Los niveles de criticidad DAL van de la A a la E; el nivel A requiere, entre otras cosas, cobertura de pruebas a nivel de condiciones individuales dentro de expresiones lógicas (MC/DC). Se considera uno de los estándares más exigentes y costosos de cumplir en la industria.

## :lock: Ciberseguridad y la cadena de suministro

Un tema relativamente nuevo para el mundo de C++: los reguladores están transfiriendo la responsabilidad de las vulnerabilidades al proveedor de software.

* :arrow_forward: **Ley de Resiliencia Cibernética de la UE (CRA)** - [digital-strategy.ec.europa.eu](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act)

    Una regulación de la UE que cubre productos con elementos digitales suministrados al mercado europeo, desde controladores industriales hasta electrónica de consumo. Requiere un desarrollo seguro, el lanzamiento de actualizaciones de seguridad durante todo el período de soporte y la notificación de vulnerabilidades explotadas activamente. Entró en vigor en diciembre de 2024, y las obligaciones principales se aplicarán a partir de finales de 2027 y las obligaciones de notificación antes. Es importante destacar que afecta no solo a las industrias "críticas para la seguridad", sino a prácticamente cualquier software que forme parte de un producto que se vende.

* :arrow_forward: **SBOM (Software Bill of Materials)** - [spdx.dev](https://spdx.dev), [cyclonedx.org](https://cyclonedx.org)

    Un inventario legible por máquina de todos los componentes y dependencias que se incluyen en el software entregado: la "lista de ingredientes", por analogía con una etiqueta en un paquete. Es necesario para que cuando se encuentre una vulnerabilidad en una biblioteca popular, puedas responder rápidamente a la pregunta "¿la tenemos?". Los dos formatos principales son SPDX y CycloneDX; ambos están estandarizados. Para C++ el tema es tangible: las dependencias a menudo se incorporan como código fuente o se compilan a mano, y sin un SBOM no siempre es obvio qué terminó exactamente en la compilación (build).

## :computer: Qué significa esto en la práctica

Si terminas en un proyecto de este tipo, lo que cambia no es tanto el lenguaje como el entorno alrededor del código:

- **Un subconjunto del lenguaje.** Algunas funciones familiares estarán prohibidas, por lo general la memoria dinámica después de la inicialización, excepciones, RTTI y a veces plantillas (templates) y la biblioteca estándar en su conjunto.
- **Análisis estático obligatorio.** La compilación falla no solo por errores del compilador sino por violaciones de las reglas. Las desviaciones de las reglas se documentan y se acuerdan por escrito, no simplemente se suprimen en el código.
- **Trazabilidad.** Para cada línea de código puedes rastrear de qué requisito provino y qué prueba la cubre. De ahí las altas exigencias sobre cómo se redactan las tareas y los commits.
- **Calificación de herramientas.** El compilador, el analizador y el framework de pruebas también deben justificarse, por lo que las versiones se actualizan rara vez, y "solo agarrar el último GCC" no siempre es posible.
- **Revisión y documentación intensas.** El volumen de documentos adjuntos puede superar el volumen de código, y los plazos pueden exceder notablemente a los del desarrollo ordinario.

## :question: Quién necesita esto realmente

**No todos.** Si escribes juegos, aplicaciones de escritorio, backends o sistemas de trading, en la práctica lo más probable es que no te encuentres con estos estándares, y no tiene sentido estudiarlos especialmente.

El tema se vuelve obligatorio si entras en la electrónica automotriz, dispositivos médicos, aviación, espacio, transporte ferroviario o automatización industrial. Para todos los demás es suficiente saber que estos estándares existen y de qué tratan, eso es suficiente para una entrevista.

La excepción es **CRA y SBOM**. Se refieren a una gama mucho más amplia de productos que la seguridad funcional clásica, por lo que vale la pena familiarizarse con ellos incluso como un desarrollador "común" cuyos productos se venden en Europa.

---

[**A la página principal**](README.md)
