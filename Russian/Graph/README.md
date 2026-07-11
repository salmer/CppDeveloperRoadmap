# Как просматривать и редактировать дорожную карту

Дорожная карта хранится в файле [roadmap.drawio.svg](roadmap.drawio.svg) — это обычное SVG-изображение со встроенной внутрь редактируемой диаграммой [draw.io](https://www.drawio.com). Один и тот же файл является и картинкой, которую вы видите, и исходником, который вы редактируете. Экспортировать и синхронизировать больше нечего: каждый принятый pull request сразу обновляет опубликованную карту.

## Просмотр

- На сайте: [salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=ru](https://salmer.github.io/CppDeveloperRoadmap/goto/svg/?l=ru)
- На GitHub: откройте [roadmap.drawio.svg](roadmap.drawio.svg) — файл отображается как изображение.

## Редактирование

1. Сделайте форк репозитория.
2. Откройте диаграмму в одном из редакторов draw.io:
   - **Веб:** зайдите на [sketch.diagrams.net](https://sketch.diagrams.net) (интерфейс draw.io в стиле whiteboard), откройте файл из *GitHub*, авторизуйтесь и выберите `Russian/Graph/roadmap.drawio.svg` в своём форке. Сохранение делает коммит прямо в ваш форк.
   - **VS Code:** установите расширение [Draw.io Integration](https://marketplace.visualstudio.com/items?itemName=hediet.vscode-drawio) и откройте файл (работает и в браузере через github.dev — нажмите `.` в своём форке).
   - **Десктоп:** [приложение draw.io](https://www.drawio.com).
3. Создайте pull request со своими изменениями.

> :warning: Не редактируйте текст SVG вручную вне draw.io — это может удалить встроенный исходник диаграммы, и файл перестанет быть редактируемым. Файл начинается с комментария с таким же предупреждением.
