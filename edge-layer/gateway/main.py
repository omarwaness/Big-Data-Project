from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class WeatherInnerData(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    rainfall: float

class WeatherData(BaseModel):
    timestamp: int
    data: WeatherInnerData

@app.post("/sensor/weather")
def receive_weather_data(payload: WeatherData):
    print("📥 Received Weather Data:", payload.dict())

    processed = {
        "timestamp": payload.timestamp,
        "temperature": payload.data.temperature,
        "humidity": payload.data.humidity,
        "wind_speed": payload.data.wind_speed,
        "rainfall": payload.data.rainfall,
        "status": "ok"
    }

    return {"message": "Data received", "processed": processed}
