#!/bin/bash
echo "Управление трафиком Blue-Green Deployment"
echo "Nginx работает на порту 8088"
echo ""
echo "Текущая версия:"
curl -s http://localhost:8088/health | python3 -m json.tool
echo ""
echo "Команды:"
echo "  Переключить на Green: cp nginx/nginx.green.conf nginx/nginx.conf && docker compose -f nginx/docker-compose.nginx.yml restart && sleep 10"
echo "  Вернуть на Blue:     cp nginx/nginx.blue.conf nginx/nginx.conf && docker compose -f nginx/docker-compose.nginx.yml restart && sleep 10"
