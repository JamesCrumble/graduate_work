### APP

приложение messages работает на 4800 порту

### Описание

для подключения к сокету подключаемся по пути ws://127.0.0.1:4800/messages/api/v1/sms/ws
необходимо отправить header - access_token (jwt)

endpoint для отправки подключенным пользователям:
http://127.0.0.1:4800/messages/api/v1/sms/send?user_id=9bb8a6d7-f159-42e7-a35f-f7cb8cc1484b
где user_id - пользователь - кому хотим отправить сообщение
обязательно указать header - access_token чтобы сообщения не мог инициировать неавторизованный пользователь