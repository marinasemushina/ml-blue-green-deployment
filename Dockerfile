FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копирование зависимостей
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY app/ .

# Создание не-root пользователя
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Переменные окружения
ENV MODEL_VERSION=v1.0.0
ENV PORT=8080

# Открываем порт
EXPOSE 8080

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
