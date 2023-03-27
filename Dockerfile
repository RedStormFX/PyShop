# Используйте официальный образ Python
FROM python:3.9

# Установите рабочую директорию
WORKDIR /app

# Копируйте файлы с зависимостями
COPY requirements.txt .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте остальные файлы проекта
COPY . .

# Выполните миграции базы данных
RUN python manage.py migrate

# Укажите команду для запуска сервера
CMD gunicorn usaShop.wsgi:application --bind 0.0.0.0:8000
