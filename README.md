# Бот помощник в Вк и Телеграм

Бот отвечает на типичные вопросы тех-поддержки в Вконтакте и Телеграм, а вот что-то посложнее – перенаправляет на операторов. 

* Пример бота [Вконтакте](https://vk.com/im?media=&sel=-203493103)
![Пример Вконтакте](https://s221vla.storage.yandex.net/rdisk/014789cef8acad41238cb96c626750baeb9ad57f9d66bdd6a1750004b66ebc0b/605a413b/gYM6vOLH3ltThvsLhTsgmmcYu3HisyGzqeqQeVArq4ZVWoypia2_-2Vud0H93FrhyFSH2s5tgrpMOPaHV8iICQ==?uid=344477538&filename=Untitled.gif&disposition=inline&hash=&limit=0&content_type=image%2Fgif&owner_uid=344477538&fsize=572550&hid=6f11372597de1f7e797c8f2fc9825614&media_type=image&tknv=v2&etag=339b521887c95d893adec3052046fb0c&rtoken=oZkb9Fa5zPgR&force_default=yes&ycrid=na-31149a1d9c1c323142134c07f8f7d8da-downloader6e&ts=5be392dd684c0&s=ecf5ffcfffaa2c3d69a37b36c68160de8286910870e0f6eecf1b0c51fae01da0&pb=U2FsdGVkX1_xNYDWFf8560-q18i5dPjOk-XJPuSQF5X6U7w4XK1yY19J4JxZaZpHGE2JTOO2MRkwFjww5U_Mk-Ol-Wlt0tzLhWR72wgehV8)

* Пример бота в [Телеграм](https://vk.cc/c02ULR)

![Пример в Телеграм](https://s231vla.storage.yandex.net/rdisk/d64aac1307a6967bb6b54310718458e4485d12abe5748501233fa04b3dda1911/605a4301/gYM6vOLH3ltThvsLhTsgmgHXM-cE7hbVRTTeqPobE7otH5iimzlWzxEHDZtMuMsVRA3FDx91c4cjGpjS7dJhEA==?uid=344477538&filename=TG.gif&disposition=inline&hash=&limit=0&content_type=image%2Fgif&owner_uid=344477538&fsize=416665&hid=0a7269cb9c0f98d8267eefb5349d11bc&media_type=image&tknv=v2&etag=ff8bb3f6d6ca56409f5a0d2e7873c334&rtoken=zfAGsdQOlFxr&force_default=yes&ycrid=na-f8bbbd51ac370600279e74a54c8e0df5-downloader20h&ts=5be3948e60240&s=48e2931a2e684e843bef41471fe9505a5ae3aea1d696670632d7f030284944b8&pb=U2FsdGVkX1_Gy_oGuO1E00puGoFLoKoWRyemnbanUrTllYJEGI1m1LyGA1O-vb63X2EoXVod9Bka5bbkG9ZnFSmItPL82CbSBDltTWnSCxQ)

Скрипт ```main.py``` запускает бота в Вк и Телеграм.

### Как установить

У вас уже должен быть установлен Python 3. Если его нет, то установите.
Так же нужно установить необходимые пакеты:
```
pip3 install -r requirements.txt
```

### Как пользоваться скриптом

Для работы скрипта нужно создать файл ```.env``` в директории где лежит скрипт.

#### Настройки для Телеграм

1. Нужно создать бота в телеграм. Написать [Отцу ботов](https://telegram.me/BotFather):
    * /start
    * /newbot
    
2. Отец ботов попросит ввести два имени. 

    * Первое — как он будет отображаться в списке контактов, можно написать на русском. 

    * Второе — имя, по которому бота можно будет найти в поиске. 
      Должно быть английском и заканчиваться на bot (например, notification_bot)

3. Вставьте ваш токен бота в файл ```.env```:
    ```
    TELEGRAM_BOT_TOKEN='95132391:wP3db3301vnrob33BZdb33KwP3db3F1I'
    ```

4. Вам необходимо получить свой chat_id. 
Чтобы получить свой chat_id, напишите в Telegram специальному боту: [@userinfobot](https://telegram.me/userinfobot)
и вставить его в файл ```.env```:
    ```
    TELEGRAM_CHAT_ID=335031317
    ```
#### Настройки для Вконтакте

1. Получить токен группы чтобы бот мог писать от имени группы и вставить в файл ```.env```:
    ```
    VK_TOKEN='2ac03179397392e1bcff9fbd02932534c979674ba0644cb0bd2c554543a38d838a342c526e54936b2d91'
    ```

#### Настройки для DialogFlow

1. Создать аккаунт в DialogFlow и проект в нём:
    * [Как создать проект в DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/setup)
2. Получить идентификатор проекта и вставить в файл ```.env```. Нам выдали такой:
    ```
    DIALOG_FLOW_ID_PROJECT='verb3-307417'
    ```
3. Создать Агента в DialogFlow:
    * [Как создать Агента в DialogFlow](https://cloud.google.com/dialogflow/es/docs/quick/build-agent)
    * DEFAULT LANGUAGE - выбрать ```Russian - ru```

4. Создать [JSON-ключ](https://cloud.google.com/docs/authentication/getting-started) и вставить в файл ```.env```:
    ```
    GOOGLE_APPLICATION_CREDENTIALS='путь_до_json_ключа/dialog_flow_config.json'
    ```

#### Обучение бота DialogFlow готовым фразам

Вы можете обучить бота в [консоле DialogFlow](https://dialogflow.cloud.google.com/) или можно обучить
бота с помощью файла json с заготовленными вопросами и ответами:

1. Пример файла для обучения - [train_phrase_1.json](https://github.com/canto9112/verb_play/blob/master/train_phrase_1.json)

2. Пример обучения новым интентам:
    ```
    >>> python3 create_intents.py название_вашего_json_файла.json
    ```
   
### Запуск скрипта
Для запуска ботов вам необходимо запустить командную строку и перейти в каталог со скриптом:
```
>>> python3 main.py 
```

### Цели проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).