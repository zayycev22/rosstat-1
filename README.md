# Первая практика росстат
Реализована первая практика росстат. Задание - создать API которое хранит файлы на локальном устройстве. Пользователь должен уметь загружать файлы, удалять файлы, перезаписывать файлы.

## Реализовано:

* [X] Авторизация
* [X] Регистрация
* [X] Загрузка файлов
* [X] Перезаписывание файлов
* [X] Удаление файлов
* [X] Автоматическое удаление файлов системой
* [X] Скачивание файлов

# Подготовка к запуску
Склонируйте проект и в корне проектка создайте файл .env
Заполите его следующими параметрами

```bash
DB_HOST=хост базы данных, если бд на локальном устройстве - используйте host.docker.internal
DB_USER=имя пользователя
DB_PASSWORD=пароль пользователя
DB_NAME=имя бд
```
PS бд используйте на postgres

# Запуск программы
```bash
docker-compose up --build
```
