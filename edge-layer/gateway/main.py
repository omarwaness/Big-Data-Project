from fastapi import FastAPI
from models import CurrentWeather
from models import WeatherForecast
from models import SoilData

app = FastAPI()


@app.post("/sensor/weather")
def receive_weather_data(payload: CurrentWeather):
    print("✔️ Received WEATHER:", payload.timestamp)
    
    data = payload.dict()

    return {
        "message": "Weather received",
        "data": data,
        "status": "ok"
    }



@app.post("/sensor/forecast")
def receive_forecast_data(payload: WeatherForecast):
    print("✔️ Received FORECAST:", payload.timestamp)
    
    data = payload.dict()

    return {
        "message": "Forecast received",
        "data": data,
        "status": "ok"
    }



@app.post("/sensor/soil")
def receive_soil_data(payload: SoilData):
    print("✔️ Received SOIL SENSOR:", payload.timestamp)
    data = payload.dict()
    data["status"] = "ok"

    return {
        "message": "Soil data received",
        "data": data
    }

