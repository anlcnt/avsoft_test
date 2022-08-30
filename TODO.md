## TODO
- [ ] avsoft_test/parser.py:37 - Разобраться с этим недоразумением
- [ ] avsoft_test/error_handler.py:25 - Большое количество сообщений может завалить количеством потоков
- [ ] avsoft_test/error_handler.py:26 - Добавить отправку по почте, SIEM, SOAR
- [ ] avsoft_test/reader.py:17 - Здесь можно использовать какой-нибудь алгоритм поиска
- [ ] avsoft_test/reader.py:19 - Поиск слов регулярным выражением
- [ ] avsoft_test/reader.py:30 - Определение, куда записывать файл
- [ ] avsoft_test/reader.py:42 - Запись файла
- [ ] avsoft_test/reader.py:49 - Watchdod?
- [ ] rabbitmq/__init__.py:22 - Передача полного списка параметров RabbitMQ
- [ ] rabbitmq/__init__.py:29 - Отлов ошибки при создании канала
- [ ] rabbitmq/__init__.py:48 - Отлов ошибки при создании json'а
- [ ] rabbitmq/__init__.py:84 - Что-то сделать с этим
- [ ] database/__init__.py:17 - Создание базы данных при её отсутствии

## In progress
- [ ] rabbitmq/__init__.py:9 - Пусть классы сами забирают конфигурации из модуля settings.py
- [ ] Dockerfile - Завернуть модули в Docker
- [ ] generator.py:25 фильтровать регулярным выражением .css, .js, mailto и tel
- [ ] avsoft_test/compose.yml:29 volume

## Done
- [*] generator.py:31 Поиск в глубину
- [*] generator.py:66 Запись в файл