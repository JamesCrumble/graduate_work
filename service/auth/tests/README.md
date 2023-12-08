# Запуски тестов

## Работа с git

при commit валидируется:

1. merge conflicts
2. flake8

при push валидируется (запуск скрипта make func_tests_exit):

1. pytest (с поднятием контейнера)

## Подготовка окружения для запуска тестов

### запуск контейнеров для тестов (он сразу прогонит тест)

```
make run_tests_local
```

### после этого можно запускать тесты без контейнера через команду

переименовать файл .env.dev.test.example в .env.dev.test

```
cd tests/functional && python -m main
```

для запуска через контейнер необходимо переименовать файл .env.dev.test.container.example в .env.dev.test.container

так сделано для того, чтобы в docker_compose все сервисы работали на своих портах, а во вне опубликованы порты отличные от разработки

### для запуска тестов через vscode для отладки или без отладки в launch.json вставляем

```
    {
      "name": "Python: main tests",
      "type": "python",
      "request": "launch",
      "program": "main.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/tests/functional",
      "justMyCode": true
    },
```
