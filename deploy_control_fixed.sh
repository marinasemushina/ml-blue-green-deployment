#!/bin/bash

# Скрипт для управления Blue-Green деплоем

set -e

BLUE_COMPOSE="docker-compose.blue.yml"
GREEN_COMPOSE="docker-compose.green.yml"
NGINX_COMPOSE="nginx/docker-compose.nginx.yml"
NGINX_CONFIG_DIR="nginx"

echo "=== Управление Blue-Green Deployment ==="

case "$1" in
    "start")
        echo "Запуск Blue-Green deployment..."
        
        # Запускаем blue версию
        echo "Запуск Blue (v1.0.0)..."
        docker compose -f $BLUE_COMPOSE up -d
        
        # Запускаем green версию
        echo "Запуск Green (v1.1.0)..."
        docker compose -f $GREEN_COMPOSE up -d
        
        # Запускаем nginx с blue конфигурацией
        echo "Запуск Nginx (трафик на Blue)..."
        cp $NGINX_CONFIG_DIR/nginx.blue.conf $NGINX_CONFIG_DIR/nginx.conf
        docker compose -f $NGINX_COMPOSE up -d
        
        echo "Ожидание запуска сервисов..."
        sleep 10
        
        echo "Запуск завершен!"
        echo "Blue: http://localhost:8081"
        echo "Green: http://localhost:8082"
        echo "Nginx: http://localhost:80"
        ;;
    
    "switch-to-green")
        echo "Переключение трафика на Green (v1.1.0)..."
        
        # Меняем конфигурацию nginx
        cp $NGINX_CONFIG_DIR/nginx.green.conf $NGINX_CONFIG_DIR/nginx.conf
        
        # Перезапускаем nginx
        docker compose -f $NGINX_COMPOSE restart
        
        echo "Ожидание перезапуска Nginx..."
        sleep 5
        
        echo "Трафик переключен на Green!"
        ;;
    
    "switch-to-blue")
        echo "Переключение трафика на Blue (v1.0.0)..."
        
        # Меняем конфигурацию nginx
        cp $NGINX_CONFIG_DIR/nginx.blue.conf $NGINX_CONFIG_DIR/nginx.conf
        
        # Перезапускаем nginx
        docker compose -f $NGINX_COMPOSE restart
        
        echo "Ожидание перезапуска Nginx..."
        sleep 5
        
        echo "Трафик переключен на Blue!"
        ;;
    
    "status")
        echo "Статус сервисов:"
        echo ""
        
        echo "=== Blue сервис (v1.0.0) ==="
        docker compose -f $BLUE_COMPOSE ps
        
        echo ""
        echo "=== Green сервис (v1.1.0) ==="
        docker compose -f $GREEN_COMPOSE ps
        
        echo ""
        echo "=== Nginx балансировщик ==="
        docker compose -f $NGINX_COMPOSE ps
        
        echo ""
        echo "=== Проверка health ==="
        echo "Blue health:"
        curl -s http://localhost:8081/health || echo "Blue недоступен"
        
        echo ""
        echo "Green health:"
        curl -s http://localhost:8082/health || echo "Green недоступен"
        
        echo ""
        echo "Nginx health:"
        curl -s http://localhost:80/health || echo "Через nginx недоступен"
        ;;
    
    "stop")
        echo "Остановка всех сервисов..."
        
        docker compose -f $NGINX_COMPOSE down
        docker compose -f $GREEN_COMPOSE down
        docker compose -f $BLUE_COMPOSE down
        
        echo "Все сервисы остановлены!"
        ;;
    
    "logs")
        echo "Логи сервисов:"
        
        case "$2" in
            "blue")
                docker compose -f $BLUE_COMPOSE logs -f
                ;;
            "green")
                docker compose -f $GREEN_COMPOSE logs -f
                ;;
            "nginx")
                docker compose -f $NGINX_COMPOSE logs -f
                ;;
            *)
                echo "Использование: $0 logs [blue|green|nginx]"
                ;;
        esac
        ;;
    
    "test")
        echo "Запуск тестов..."
        python3 test_client.py
        ;;
    
    *)
        echo "Использование: $0 {start|stop|status|switch-to-blue|switch-to-green|logs|test}"
        echo ""
        echo "Команды:"
        echo "  start              - Запуск всех сервисов"
        echo "  stop               - Остановка всех сервисов"
        echo "  status             - Показать статус сервисов"
        echo "  switch-to-blue     - Переключить трафик на Blue"
        echo "  switch-to-green    - Переключить трафик на Green"
        echo "  logs [service]     - Показать логи сервиса"
        echo "  test               - Запустить тесты"
        exit 1
        ;;
esac
