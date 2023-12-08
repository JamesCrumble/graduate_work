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
