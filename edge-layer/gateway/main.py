from fastapi import FastAPI

from models import CurrentWeather
from models import WeatherForecast
from models import SoilData

from preprocess.feature_extraction import clean_weather
from preprocess.feature_extraction import clean_forecast

from preprocess.edge_validation import validate_weather
from preprocess.edge_validation import validate_forecast
from preprocess.edge_validation import validate_soil

app = FastAPI()


@app.post("/sensor/weather")
def receive_weather_data(payload: CurrentWeather):
    try:
        print("✔️ Received WEATHER:", payload.timestamp)
    
        data = clean_weather(payload)
        data = validate_weather(data)

        return {
            "message": "Weather received",
            "data": data.dict(),
            "status": "ok"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.post("/sensor/forecast")
def receive_forecast_data(payload: WeatherForecast):
    try:
        print("✔️ Received FORECAST:", payload.timestamp)
    
        data = clean_forecast(payload)
        data = validate_forecast(data)

        return {
            "message": "Forecast received",
            "data": data.dict(),
            "status": "ok"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/sensor/soil")
def receive_soil_data(payload: SoilData):
    try:
        print("✔️ Received SOIL SENSOR:", payload.timestamp)
    
        data = validate_soil(payload)

        return {
            "message": "Soil data received",
            "data": data.dict(),
            "status": "ok"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




