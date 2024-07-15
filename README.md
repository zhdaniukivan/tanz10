# Project mane tanz10

## Установка и запуск проекта

### Шаг 1: Клонирование репозитория и переход в диреторию с проектом
git clone https://github.com/zhdaniukivan/tanz10.git
cd tanz10

### Шаг 2: Запускаем виртуальное окружение
pip install virtualenv
virtualenv .venv
source .venv/bin/activate

### Шаг 3: Установка необходимых зависимостей
pip install -r requirements.txt

### Шаг 4: Настройка базы данных в Docker контейнере
Загрузите образ PostgreSQL:
sudo docker pull postgres

Запустите контейнер PostgreSQL, заменив 'POSTGRES_USER' и 'POSTGRES_PASSWORD' на ваши данные:

sudo docker run -itd \
  -e POSTGRES_USER='POSTGRES_USER' \
  -e POSTGRES_PASSWORD='POSTGRES_PASSWORD' \
  -p 5432:5432 \
  -v /path/to/your/local/data:/var/lib/postgresql/data \
  postgres:latest

Для резервного копирования данных мы также смонтировали каталог /var/lib/postgresql/data в каталог /data на хост-машине контейнера postgres.

Посмотрите активные контейнеры:
sudo docker ps

Найдите ваш контейнер с PostgreSQL и скопируйте его ID(ниже пример моего выводв мой id это 99b22c29b460):
99b22c29b460   postgres:latest   "docker-entrypoint.s…"   19 minutes ago   Up 19 minutes   0.0.0.0:5433->5432/tcp, :::5433->5432/tcp   great_dijkstra

Запустите bash в Docker контейнере, используя ID контейнера:
sudo docker exec -it 99b22c29b460 bash

Запустите оболочку PostgreSQL:
psql -U POSTGRES_USER

Создайте базу данных (замените "mydatabase" на название вашей базы данных):
CREATE DATABASE 'mydatabase';

Выйдите из PostgreSQL:
\q

Выйдите из Docker контейнера:
exit

### Шаг 5: Настройка конфигурации
Переименуйте файл example.env в .env и заполните файл .env вашими данными:

DATABASE_USER = "DATABASE_USER"
PASSWORD = "PASSWORD"
DATABASE_NAME = "DATABASE_NAME"

### Шаг 6: Запуск приложения
python app.py
Приложение будет доступно по адресам http://127.0.0.1:5000 и http://127.0.0.1:5000/data

### Шаг 7: Запуск тестов
pytest test_app.py
