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


def fetch_full_weather_data():
    """Fetch full raw OpenWeather response."""
    try:
        resp = requests.get(WEATHER_URL, timeout=5)
        resp.raise_for_status()

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "raw_weather": resp.json()
        }

    except Exception as e:
        print("❌ Failed to fetch weather data:", e)
        return None


def run_weather_sensor():
    print("🌤️ Weather Sender Started...")
    #print("Gateway URL:", GATEWAY_URL)

    while True:
        payload = fetch_full_weather_data()

        if payload:
            try:
                response = requests.post(GATEWAY_URL, json=payload, timeout=5)
                print("Sent full weather payload | Gateway response:", response.json())
            except Exception as e:
                print("❌ Failed to send weather data:", e)
        else:
            print("⚠️ Skipping sending due to fetch error.")

        time.sleep(5)