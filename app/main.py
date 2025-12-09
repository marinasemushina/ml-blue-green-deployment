from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pickle
import numpy as np
import os
import logging
from typing import Dict, Any

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создание приложения
app = FastAPI(
    title="Iris Classification API",
    description="API для классификации цветов ириса с Blue-Green Deployment",
    version=os.getenv("MODEL_VERSION", "v1.0.0")
)

# Загрузка модели при старте
MODEL_PATH = "iris_classifier_pipeline.pkl"
model = None
model_version = os.getenv("MODEL_VERSION", "v1.0.0")

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    logger.info(f"Model {model_version} loaded successfully from {MODEL_PATH}")
    if hasattr(model, 'classes_'):
        logger.info(f"Model classes: {model.classes_}")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

# Модели данных
class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., ge=0, le=10, description="Длина чашелистика (см)")
    sepal_width: float = Field(..., ge=0, le=10, description="Ширина чашелистика (см)")
    petal_length: float = Field(..., ge=0, le=10, description="Длина лепестка (см)")
    petal_width: float = Field(..., ge=0, le=10, description="Ширина лепестка (см)")

class PredictResponse(BaseModel):
    prediction: str
    probabilities: Dict[str, float]
    version: str

class HealthResponse(BaseModel):
    status: str
    version: str
    model_loaded: bool

# Эндпоинты
@app.get("/")
async def root():
    return {
        "message": "Iris Classification API",
        "version": model_version,
        "endpoints": ["/health", "/predict", "/model-info", "/examples"]
    }

@app.get("/health", response_model=HealthResponse)
async def health():
    """Проверка здоровья сервиса"""
    return {
        "status": "healthy" if model else "unhealthy",
        "version": model_version,
        "model_loaded": model is not None
    }

@app.get("/model-info")
async def model_info():
    """Информация о модели"""
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    info = {
        "version": model_version,
        "model_type": type(model).__name__,
        "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
        "classes": ["setosa", "versicolor", "virginica"]
    }
    
    if hasattr(model, 'classes_'):
        info["model_classes"] = model.classes_.tolist()
    
    return info

@app.post("/predict", response_model=PredictResponse)
async def predict(features: IrisFeatures):
    """Предсказание класса ириса"""
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Подготавливаем данные
        input_data = np.array([[
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width
        ]])
        
        # Предсказание
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        
        # Имена классов
        class_names = ["setosa", "versicolor", "virginica"]
        predicted_class = class_names[prediction]
        
        # Вероятности
        prob_dict = {
            class_names[i]: float(probabilities[i])
            for i in range(len(class_names))
        }
        
        logger.info(f"Prediction: {predicted_class} with probabilities {prob_dict}")
        
        return {
            "prediction": predicted_class,
            "probabilities": prob_dict,
            "version": model_version
        }
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/examples")
async def get_examples():
    """Примеры запросов для тестирования"""
    return {
        "examples": [
            {
                "description": "Iris Setosa (пример)",
                "request": {
                    "sepal_length": 5.1,
                    "sepal_width": 3.5,
                    "petal_length": 1.4,
                    "petal_width": 0.2
                }
            },
            {
                "description": "Iris Versicolor (пример)",
                "request": {
                    "sepal_length": 6.0,
                    "sepal_width": 2.7,
                    "petal_length": 5.1,
                    "petal_width": 1.6
                }
            },
            {
                "description": "Iris Virginica (пример)",
                "request": {
                    "sepal_length": 6.9,
                    "sepal_width": 3.1,
                    "petal_length": 5.4,
                    "petal_width": 2.1
                }
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
