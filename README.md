# Blue-Green Deployment для ML модели классификации ирисов

Проект демонстрирует стратегию Blue-Green Deployment для ML модели с использованием Docker, FastAPI и Nginx.

## Структура проекта
```
ml-blue-green-deployment/
├── app/ # Приложение FastAPI
│ ├── main.py # Основное приложение
│ ├── requirements.txt # Зависимости Python
│ ├── create_model.py # Создание моделей
│ ├── iris_classifier_v1.pkl # Модель Blue (v1.0.0)
│ ├── iris_classifier_v2.pkl # Модель Green (v1.1.0)
│ ├── iris_classifier_blue.pkl # Ссылка на Blue модель
│ └── iris_classifier_green.pkl # Ссылка на Green модель
├── nginx/ # Конфигурация балансировщика
│ ├── nginx.conf # Активная конфигурация
│ ├── nginx.blue.conf # Конфигурация для Blue
│ ├── nginx.green.conf # Конфигурация для Green
│ └── docker-compose.nginx.yml # Docker для Nginx
├── docker-compose.blue.yml # Docker Compose для Blue
├── docker-compose.green.yml # Docker Compose для Green
├── Dockerfile # Docker образ приложения
├── deploy_control.sh # Скрипт управления деплоем
├── test_client.py # Тестовый клиент
└── README.md # Документация

```

## Быстрый старт

### 1. Установка зависимостей
```bash
cd app
pip install -r requirements.txt
```
### 2. Создание моделей
```bash
cd app
python3 create_model.py
cd ..
```
### 3. Запуск сервисов
```
./deploy_control.sh start
```
### 4. Проверка работы
```
./deploy_control.sh test
```
### 5. Управление деплоем
```
# Переключить на Green
./deploy_control.sh switch-to-green

# Вернуть на Blue
./deploy_control.sh switch-to-blue

# Остановить все
./deploy_control.sh stop
```
### API эндпоинты
GET /health - проверка работоспособности

POST /predict - предсказание класса ириса

GET /model-info - информация о модели

### Примеры запросов
### Проверка здоровья
```
curl http://localhost:8088/health
```
### Предсказание
```
curl -X POST http://localhost:8088/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```
### Мониторинг

Логи Blue: ./deploy_control.sh logs blue

Логи Green: ./deploy_control.sh logs green

Логи Nginx: ./deploy_control.sh logs nginx

### CI/CD Pipeline

Проект включает GitHub Actions workflow для автоматического тестирования и деплоя. При пуше в ветку main:

Запускаются тесты модели

Собираются Docker образы для Blue и Green версий

Образы публикуются в GitHub Container Registry

Симулируется процесс деплоя

### Blue-Green стратегия

#### Blue версия (v1.0.0)

RandomForest с 100 деревьями

max_depth=3

Порт: 8081

### Green версия (v1.1.0)

Улучшенный RandomForest с 200 деревьями

max_depth=5

Порт: 8082

### Переключение трафика

По умолчанию трафик идет на Blue

Для переключения на Green: ./deploy_control.sh switch-to-green

Для отката на Blue: ./deploy_control.sh switch-to-blue

### Скриншоты работы
Скриншоты работы проекта находятся в папке screenshots и описаны в файле SCREENSHOTS.md.
