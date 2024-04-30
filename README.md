# Бот поддержки пользователей

## Описание
Этот репозиторий содержит код для ботов, работающих с VK и Telegram. Боты используют Dialogflow для обработки естественного языка и отвечают на сообщения пользователей.

## Функции
- **vk_bot.py**: Отвечает на сообщения пользователей во ВКонтакте, используя Dialogflow.
- **tg_bot.py**: Отслеживает ошибки VK бота и отправляет уведомления о них в Telegram.
- **add_dialogflow_intent.py**: Обучает нейросеть диалогам 

## Начало работы
Чтобы начать использовать этих ботов, вам нужно выполнить следующие шаги:

### Предварительные требования
1. Установите Python 3.
2. Скачайте [репозиторий](https://github.com/KillerBee88/Support_Bot)
3. Установите необходимые пакеты через pip:
    ```console
    pip install -r requirements.txt
    ```

### Настройка
#### Работа с DialogFlow
1. Создайте проект на странице [DialogFlow](https://dialogflow.cloud.google.com/#/login). При создании проекта у Вас появится идентификатор проекта для дальнейшей работы с DialogFlow.
2.  Далее нужно создать [агента](https://cloud.google.com/dialogflow/es/docs/quick/build-agent), обязательно с русским языком.
3. После этих действий нужно [включить](https://cloud.google.com/dialogflow/es/docs/quick/setup#api) API DialogFlow, и получить json файл с [GOOGLE_APPLICATION_CREDENTIALS](https://support.woztell.com/portal/en/kb/articles/how-to-get-the-json-key-file-from-dialogflow) 
#### Тренировка бота DialogFlow
В корне проекта есть скрипт, который позволяет тренировать бота запуском команды
````console
python3 add_dialogflow_intent.py
````
#### Создание API ключа вк и группы
1. Создайте группу во Вконтакте
2. На вкладке управления группы найдите "Работа с API", и создайте ключи. Так же нужно разрешить боту отправку сообщений.
#### Ключи
1. Создайте файл `.env` в корне проекта с следующим содержанием:
    ```
    VK_BOT_TOKEN=<ваш_vk_токен>
    TELEGRAM_BOT_TOKEN=<ваш_telegram_токен>
    TELEGRAM_CHAT_ID=<ваш_telegram_chat_id>
    GOOGLE_APPLICATION_CREDENTIALS=<путь_к_файлу_с_ключами_dialogflow>
    DIALOGFLOW_PROJECT_ID=<ваш_dialogflow_project_id>
    ```
2. Замените значения в угловых скобках на ваши реальные данные.


### Запуск
Для запуска VK бота выполните:
````console
python3 vk_bot.py
````
Для запуска Telegram бота выполните:
````console
python3 tg_bot.py
````
Для обучения нейросети нужно выполнить команду:
````console
python3 add_dialogflow_intent.py путь/к/файлу.json
````
## Пример работы ботов
[tg_bot.py:](https://t.me/BotTranscriBot)

![tgbot](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExeWN4Zjl2bG1mZnJjMWN2ajRtdnFhNDZ0cGY2aDNsZDUyZW5oMTFlNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/zWQIwDRfc9RqSIeeTV/giphy.gif)

[vk_bot.py:](https://vk.com/im?peers=c11&sel=-225735422)

![vkbot](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTEybTRrMTdwZDA0c201cmk1a2Y3NmhsYTI4MnFpb2VteW5oejFuayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/iDGK6hB4c5LfGDN2oW/giphy.gif)
