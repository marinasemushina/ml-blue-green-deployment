import pickle
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import os

def create_model_v1():
    """Создание модели версии 1.0.0"""
    print("Создание модели v1.0.0...")
    
    # Загрузка данных
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Разделение на train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Создание пайплайна для v1.0.0
    pipeline_v1 = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(
            n_estimators=100, 
            random_state=42,
            max_depth=3
        ))
    ])
    
    # Обучение модели
    pipeline_v1.fit(X_train, y_train)
    
    # Оценка точности
    train_score = pipeline_v1.score(X_train, y_train)
    test_score = pipeline_v1.score(X_test, y_test)
    
    # Сохранение модели
    with open('iris_classifier_v1.pkl', 'wb') as f:
        pickle.dump(pipeline_v1, f)
    
    print("Модель v1.0.0 сохранена в iris_classifier_v1.pkl")
    print(f"Точность на обучении: {train_score:.4f}")
    print(f"Точность на тесте: {test_score:.4f}")
    
    return pipeline_v1

def create_model_v2():
    """Создание улучшенной модели версии 1.1.0"""
    print("\nСоздание модели v1.1.0...")
    
    # Загрузка данных
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Разделение на train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Создание улучшенного пайплайна для v1.1.0
    pipeline_v2 = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', RandomForestClassifier(
            n_estimators=200,      # Больше деревьев
            random_state=42,
            max_depth=5,           # Большая глубина
            min_samples_split=2,
            min_samples_leaf=1
        ))
    ])
    
    # Обучение модели
    pipeline_v2.fit(X_train, y_train)
    
    # Оценка точности
    train_score = pipeline_v2.score(X_train, y_train)
    test_score = pipeline_v2.score(X_test, y_test)
    
    # Сохранение модели
    with open('iris_classifier_v2.pkl', 'wb') as f:
        pickle.dump(pipeline_v2, f)
    
    print("Модель v1.1.0 сохранена в iris_classifier_v2.pkl")
    print(f"Точность на обучении: {train_score:.4f}")
    print(f"Точность на тесте: {test_score:.4f}")
    
    return pipeline_v2

def main():
    print("=" * 50)
    print("Создание моделей для Blue-Green Deployment")
    print("=" * 50)
    
    # Создаем обе версии моделей
    model_v1 = create_model_v1()
    model_v2 = create_model_v2()
    
    # Создаем символические ссылки
    print("\nСоздание символических ссылок...")
    
    if os.path.exists('iris_classifier_v1.pkl'):
        if os.path.exists('iris_classifier_blue.pkl'):
            os.remove('iris_classifier_blue.pkl')
        os.symlink('iris_classifier_v1.pkl', 'iris_classifier_blue.pkl')
        print("Создана ссылка: iris_classifier_blue.pkl → iris_classifier_v1.pkl")
    
    if os.path.exists('iris_classifier_v2.pkl'):
        if os.path.exists('iris_classifier_green.pkl'):
            os.remove('iris_classifier_green.pkl')
        os.symlink('iris_classifier_v2.pkl', 'iris_classifier_green.pkl')
        print("Создана ссылка: iris_classifier_green.pkl → iris_classifier_v2.pkl")
    
    print("\n" + "=" * 50)
    print("Все модели успешно созданы!")
    print("=" * 50)

if __name__ == "__main__":
    main()
