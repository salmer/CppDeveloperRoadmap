# Как просматривать и редактировать дорожную карту

[roadmap.drawio.svg](roadmap.drawio.svg) — это обычное SVG-изображение со встроенной диаграммой
[draw.io](https://www.drawio.com): откройте его где угодно, чтобы увидеть карту. Но это
**сгенерированный** файл: настоящий исходник — это языконезависимое текстовое описание в
[`tools/mapgen/roadmap/`](../../tools/mapgen/roadmap), а этот `.drawio.svg` является результатом
сборки, а не тем, что вы правите.

## Просмотр

- На сайте: [salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=ru](https://salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=ru)
- На GitHub: откройте [roadmap.drawio.svg](roadmap.drawio.svg) — файл отображается как изображение.
- Интерактивно: [просмотрщик draw.io](https://salmer.github.io/CppDeveloperRoadmap/goto/drawio/?l=ru) (только просмотр — изменения там не сохраняются).

## Редактирование

Карта собирается из `tools/mapgen/roadmap/` — `structure.dsl` (дерево узлов, грейды, этапы,
подсказки) и по одному `<lang>.tsv` на язык (только текст). **Не редактируйте этот `.drawio.svg`
вручную** — он пересобирается из исходника, и CI (`mapcheck`) отклонит карту, которая
разошлась с исходником.

1. Сделайте форк и правьте исходник:
   - узел, его грейд/этап или подсказка → `tools/mapgen/roadmap/structure.dsl`
   - текст (подпись, подсказка, дата) → соответствующая строка в `en.tsv` / `ru.tsv` / `zh.tsv`
     (новому узлу нужна строка **во всех трёх**).
2. Пересоберите и скопируйте карты (нужны Python + Pillow + десктопный CLI draw.io):
   ```bash
   pip install -r tools/mapgen/requirements.txt
   python tools/mapgen/build.py --dir tools/mapgen/roadmap --langs en,ru,zh
   cp tools/mapgen/roadmap/en.drawio.svg English/Graph/roadmap.drawio.svg
   cp tools/mapgen/roadmap/ru.drawio.svg Russian/Graph/roadmap.drawio.svg
   cp tools/mapgen/roadmap/zh.drawio.svg Chinese/Graph/roadmap.drawio.svg
   ```
3. Проверьте: `python tools/mapcheck/check.py --no-date` (0 жёстких ошибок), затем создайте
   pull request с исходником **и** пересобранными картами.

Грамматика DSL и подробности — в [`tools/mapgen/README.md`](../../tools/mapgen/README.md). Не
можете запустить сборку? Всё равно поправьте исходник и укажите это в PR — мейнтейнер
пересоберёт карты.
