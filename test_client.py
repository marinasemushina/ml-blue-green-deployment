import requests
import json
import time

def test_endpoint(url, name):
    """Тестирование эндпоинта"""
    print(f"\n{'='*50}")
    print(f"Тестирование {name}: {url}")
    print(f"{'='*50}")
    
    try:
        response = requests.get(url, timeout=5)
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return True
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return False

def test_predict(url, data):
    """Тестирование предсказания"""
    print(f"\nТестирование предсказания: {url}")
    
    try:
        response = requests.post(url, json=data, timeout=5)
        print(f"Статус: {response.status_code}")
        print(f"Ответ: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return True
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return False

def main():
    # Тестируем разные сервисы
    services = [
        ("Blue сервис (v1.0.0)", "http://localhost:8081"),
        ("Green сервис (v1.1.0)", "http://localhost:8082"),
        ("Nginx балансировщик", "http://localhost:80")
    ]
    
    # Пример данных для предсказания
    test_data = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    
    print("Тестирование Blue-Green Deployment")
    print("="*50)
    
    # Тестируем health эндпоинты
    for name, base_url in services:
        test_endpoint(f"{base_url}/health", name)
        test_endpoint(f"{base_url}/model-info", f"{name} - model info")
    
    # Тестируем предсказания
    print(f"\n{'='*50}")
    print("Тестирование предсказаний")
    print(f"{'='*50}")
    
    for name, base_url in services:
        print(f"\n{name}:")
        test_predict(f"{base_url}/predict", test_data)
    
    # Получаем примеры
    print(f"\n{'='*50}")
    print("Получение примеров данных")
    print(f"{'='*50}")
    
    for name, base_url in services:
        test_endpoint(f"{base_url}/examples", f"{name} - примеры")

if __name__ == "__main__":
    main()
