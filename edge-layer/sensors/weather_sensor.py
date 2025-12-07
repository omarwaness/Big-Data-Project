import os
from dotenv import load_dotenv
import requests
import time
from datetime import datetime

load_dotenv()

# Gateway URL
BASE_URL = os.getenv("GATEWAY_BASE_URL")
GATEWAY_URL = BASE_URL + "/weather"

# OpenWeather API details
COUNTRY = os.getenv("LOCATION")
API_KEY = os.getenv("API_KEY_OPENWEATHER")
WEATHER_URL = os.getenv("WEATHER_ENDPOINT_OPENWEATHER") + f"?q={COUNTRY}&appid={API_KEY}&units=metric"

def generate_weather_data():
    try:
        resp = requests.get(WEATHER_URL, timeout=5)
        resp.raise_for_status()
        weather = resp.json()

        data = {
            "temperature": weather["main"]["temp"],
            "humidity": weather["main"]["humidity"],
            "wind_speed": weather["wind"]["speed"],
            "rainfall": weather.get("rain", {}).get("1h", 0)
        }

        return {
            "timestamp": int(time.time()),
            "data": data
        }
    except Exception as e:
        print("❌ Failed to fetch weather data:", e)
        return None

def main():
    print("Gateway URL:", GATEWAY_URL)
    print("🌤️ Weather Sensor Started...")

    while True:
        weather_payload = generate_weather_data()
        if weather_payload:
            try:
                response = requests.post(GATEWAY_URL, json=weather_payload, timeout=5)
                print("Sent:", weather_payload, "| Gateway Status:", response.json())
            except Exception as e:
                print("❌ Failed to send data:", e)
        else:
            print("⚠️ Skipping sending due to fetch error.")

        time.sleep(5)

if __name__ == "__main__":
    main()
