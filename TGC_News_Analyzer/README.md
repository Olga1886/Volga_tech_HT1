# Telegram News Channels Analyzer


Это приложение Python для анализа содержания новостных телеграм-каналов. Оно принимает на вход HTML-файл, экспортированный из Telegram, и создает CSV-файл с результатами анализа. При наличии параметра `--timeline_output` также создается файл со сводной информацией по датам. При наличии параметра `--plot_output` создается PNG файл с визуализацией сводных данных.


## Установка


Убедитесь, что у вас установлен Python 3.6+.


Установите зависимости, используя файл `requirements.txt`:


1.  **Создайте файл:** В вашей папке проекта (например, `C:\Users\YourUserName\YourProjectFolder\TGC_News_Analyzer`) создайте новый файл с именем `requirements.txt`. Обратите внимание, что путь к папке проекта будет зависеть от вашей системы и где вы расположили папку проекта.
2.  **Скопируйте содержимое:** Скопируйте следующий список библиотек в файл `requirements.txt`:


    ```
    beautifulsoup4
    requests
    lxml
    scikit-learn
    nltk
    vaderSentiment
    matplotlib
    ```
3.  **Установите зависимости:** В терминале, перейдя в вашу папку проекта (например, `C:\Users\YourUserName\YourProjectFolder\TGC_News_Analyzer`), выполните следующую команду:


    ```
    pip install -r requirements.txt
    ```


## Использование


Для запуска приложения используйте следующие команды:


**Для создания `output.csv`:**


python cli.py --input_file messages.html --output_file output.csv


Для создания output.csv и timeline.csv:


python cli.py --input_file messages.html --output_file output.csv --timeline_output timeline.csv


Для создания output.csv , timeline.csv и timeline.png:


python cli.py --input_file messages.html --output_file output.csv --timeline_output timeline.csv --plot_output timeline.png


--input_file: Путь к HTML-файлу (messages.html).


--output_file: Путь к выходному CSV-файлу с анализом (output.csv).


--timeline_output: (необязательный) Путь к выходному CSV-файлу с таймлайном (timeline.csv).


--plot_output: (необязательный) Путь к файлу для сохранения графика таймлайна (timeline.png).


После запуска скрипта будут сгенерированы соответствующие файлы.


Примеры использования


Пример 1: Анализ сообщений и сохранение результатов в CSV:


python cli.py --input_file messages.html --output_file output.csv
content_copy


Этот пример проанализирует messages.html и сохранит результаты в output.csv.


Пример 2: Анализ сообщений, создание таймлайна и сохранение в CSV:


python cli.py --input_file messages.html --output_file output.csv --timeline_output timeline.csv


Этот пример проанализирует messages.html, сохранит результаты в output.csv, и создаст таймлайн в timeline.csv.


Пример 3: Анализ сообщений, создание таймлайна в CSV и PNG:


python cli.py --input_file messages.html --output_file output.csv --timeline_output timeline.csv --plot_output timeline.png


Этот пример проанализирует messages.html, сохранит результаты в output.csv, создаст таймлайн в timeline.csv и сгенерирует график в timeline.png.


Дополнительно:


Для того чтобы использовать метод bag_of_words для категоризации и text_classification с обучением модели используйте параметр --method.


--method bag_of_words - использование метода мешка слов.


--method text_classification - использование метода классификации текста.


python cli.py --input_file messages.html --output_file output.csv --method bag_of_words


python cli.py --input_file messages.html --output_file output.csv --method text_classification


python cli.py --input_file messages.html --output_file output.csv --timeline_output timeline.csv  --plot_output timeline.png --method text_classification


python cli.py --input_file messages.html --output_file output.csv --timeline_output timeline.csv --method bag_of_words


Инструкция по запуску и тестированию:


1. Подготовка:


Получите файл messages.html: Вам нужен HTML-файл, содержащий историю сообщений из телеграм-канала. Чтобы его получить:


Откройте Telegram на компьютере или в веб-версии.


Перейдите в нужный вам канал.


Нажмите на три вертикальные точки (меню) и выберите "Экспорт истории чата" (или аналогичный пункт).


В открывшемся окне экспорта выберите формат "HTML" и нажмите "Экспортировать".


Сохраните полученный файл messages.html в папку вашего проекта (например, C:\Users\YourUserName\YourProjectFolder\TGC_News_Analyzer). Обратите внимание, что путь к папке проекта и имя пользователя будут зависеть от вашей системы.


Установите зависимости: создайте файл requirements.txt с указанным содержимым, и запустите команду pip install -r requirements.txt в терминале, перейдя в папку проекта.


2.  Запуск:


Откройте терминал или командную строку, перейдите в папку проекта TGC_News_Analyzer (например, C:\Users\YourUserName\YourProjectFolder\TGC_News_Analyzer).


Выполните одну из команд, как в примерах выше.


3.  Проверка результатов:


Убедитесь, что в папке проекта создались файлы output.csv, а также timeline.csv (если вы указали --timeline_output) и timeline.png (если вы указали --plot_output).


Откройте CSV-файлы в любом текстовом редакторе или табличном процессоре (например, Excel) и убедитесь, что данные сохранены и структурированы корректно.


Откройте timeline.png, если вы его создавали, и посмотрите на график.
