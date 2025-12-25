from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from models import CurrentWeather
from models import WeatherForecast
from models import SoilData

from preprocess.feature_extraction import clean_weather
from preprocess.feature_extraction import clean_forecast

from preprocess.edge_validation import validate_weather
from preprocess.edge_validation import validate_forecast
from preprocess.edge_validation import validate_soil

from kafka_producer import send_to_kafka, create_kafka_producer


kafka_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global kafka_client
    print("🚀 Starting up: Initializing Kafka Producer...")
    kafka_client = create_kafka_producer()

    yield
    print("🛑 Shutting down: Closing Kafka Producer...")
    if kafka_client is not None:
        kafka_client.close()
    print("✔️ Kafka connection closed.")

app = FastAPI(lifespan=lifespan)


@app.post("/sensor/weather")
def receive_weather_data(payload: CurrentWeather):
    try:
        print("✔️ Received WEATHER:", payload.timestamp)
    
        data = clean_weather(payload)
        data = validate_weather(data)

        success = send_to_kafka(
            producer=kafka_client, 
            topic='farm-weather', 
            data=data.dict()
        )

        if not success:
            raise HTTPException(status_code=500, detail="Kafka streaming failed")

        return {
            "status": "ok",
            "topic": "farm-weather",
            "message": "Weather data sent to Kafka"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.post("/sensor/forecast")
def receive_forecast_data(payload: WeatherForecast):
    try:
        print("✔️ Received FORECAST:", payload.timestamp)
    
        data = clean_forecast(payload)
        data = validate_forecast(data)

        success = send_to_kafka(
            producer=kafka_client, 
            topic='farm-forecast', 
            data=data.dict()
        )

        if not success:
            raise HTTPException(status_code=500, detail="Kafka streaming failed")

        return {
            "status": "ok",
            "topic": "farm-forecast",
            "message": "Forecast data sent to Kafka"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/sensor/soil")
def receive_soil_data(payload: SoilData):
    try:
        print("✔️ Received SOIL SENSOR:", payload.timestamp)
    
        data = validate_soil(payload)

        success = send_to_kafka(
            producer=kafka_client, 
            topic='farm-soil', 
            data=data.dict()
        )

        if not success:
            raise HTTPException(status_code=500, detail="Kafka streaming failed")

        return {
            "status": "ok",
            "topic": "farm-soil",
            "message": "Soil data sent to Kafka"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

