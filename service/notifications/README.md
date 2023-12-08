### APP

сервис notifications API работает на 4777 порту

### OpenAPI

доступна по ссылке http://127.0.0.1:4777/notifications/api/openapi

### Создание уведомления

Созданы endpoint-ы для отправки уведомления через Email и web push (для ws),
подразумевается, что под каждый вид (Email, SMS, WatsAPP ...) будет свой endpoint
и своя очередь

#### Тело сообщения:

```
{
  "is_broadcast": bool, - используется для рассылки всем пользователям
  "template_id": number, - идентификатор шаблона
  "user_ids": [str], - список пользователей, если не is_broadcast
  "context": dict[str,any] - полезная нагрузка для генерации шаблона
}
```

### Sentry

проверка работы sentry http://127.0.0.1:4600/activity/api/error
