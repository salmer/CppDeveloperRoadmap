# Cómo ver y editar la hoja de ruta

[roadmap.drawio.svg](roadmap.drawio.svg) es una imagen SVG normal con un diagrama de [draw.io](https://www.drawio.com) incrustado: ábrela en cualquier lugar para ver el mapa. Es **generada**: el código fuente real es una descripción de texto neutral al idioma en [`tools/mapgen/roadmap/`](../../tools/mapgen/roadmap), por lo que este `.drawio.svg` es el resultado de la compilación, no lo que debes editar.

## Visualización

- En el sitio: [salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=es](https://salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=es)
- En GitHub: abre [roadmap.drawio.svg](roadmap.drawio.svg) — se renderiza como una imagen.
- Interactivamente: el [visor de draw.io](https://salmer.github.io/CppDeveloperRoadmap/goto/drawio/?l=es) (solo lectura — los cambios allí no se guardan).

## Edición

El mapa se construye a partir de `tools/mapgen/roadmap/` — `structure.dsl` (el árbol de nodos, grados, etapas, cuadros de sugerencias) y un `<lang>.tsv` por idioma (solo el texto). **No edites este `.drawio.svg` a mano** — se regenera a partir de la fuente, y el CI (`mapcheck`) rechaza un mapa que se haya desviado de ella.

1. Haz un fork del repositorio y edita la fuente:
   - un nodo, su grado/etapa, o una sugerencia → `tools/mapgen/roadmap/structure.dsl`
   - el texto (una etiqueta, una sugerencia, la fecha) → la fila correspondiente en `en.tsv` / `ru.tsv` / `zh.tsv` / `es.tsv`
     (un nuevo nodo necesita una fila en **todos ellos**).
2. **Solo la primera vez** — prepara tu máquina:
   ```bash
   python tools/mapgen/setup.py --venv
   ```
   Crea un virtualenv, instala Pillow y verifica las dos cosas que no puede instalar por ti (una fuente CJK y la aplicación de escritorio draw.io), imprimiendo el comando exacto para tu sistema operativo si falta alguna.
3. Reconstruye, actualiza todos los mapas y valida — un comando desde la raíz del repositorio:
   ```bash
   python tools/mapgen/build.py --dir tools/mapgen/roadmap --deploy --check
   ```
   `--deploy` copia cada mapa construido sobre su `<Language>/Graph/roadmap.drawio.svg`;
   `--check` ejecuta `mapcheck` después. Las dependencias se vuelven a verificar antes de construir nada, por lo que una faltante — o un virtualenv que olvidaste activar — se informa por adelantado.
4. Abre un pull request con la fuente **y** los mapas regenerados.

Consulta [`tools/mapgen/README.md`](../../tools/mapgen/README.md) para la gramática del DSL y detalles.
¿No puedes ejecutar la compilación? Edita la fuente de todos modos y anótalo en tu PR — un mantenedor regenerará los mapas.
