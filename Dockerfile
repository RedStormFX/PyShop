# Используйте официальный образ Python
FROM python:3.11-slim

# Установите рабочую директорию
WORKDIR /app

# Копируйте файлы с зависимостями и установите их
COPY requirements.txt /app/
COPY .env /app/

RUN pip install --no-cache-dir -r requirements.txt

# Копируйте остальные файлы приложения
COPY . /app/

# Экспортируйте переменные окружения
ENV DJANGO_SETTINGS_MODULE=usaShop.settings
ENV PYTHONUNBUFFERED=1

# Соберите статические файлы
RUN python manage.py collectstatic --noinput

# Выполните миграции базы данных
RUN python manage.py migrate

# Откройте порт для приложения
EXPOSE 8080

# Запустите приложение
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:8080", "usaShop.wsgi:application"]

