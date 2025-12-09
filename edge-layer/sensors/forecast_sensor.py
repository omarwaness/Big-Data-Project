import os
import time
import requests
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

# Gateway endpoint for forecast
BASE_URL = os.getenv("GATEWAY_BASE_URL")
GATEWAY_URL = BASE_URL + "/forecast"

# OpenWeather forecast details
COUNTRY = os.getenv("LOCATION")
API_KEY = os.getenv("API_KEY_OPENWEATHER")
FORECAST_URL = (
    os.getenv("FORECAST_ENDPOINT_OPENWEATHER") +
    f"?q={COUNTRY}&appid={API_KEY}&units=metric"
)


def fetch_raw_forecast():
    """
    Fetch full raw forecast JSON from OpenWeather.
    """
    try:
        resp = requests.get(FORECAST_URL, timeout=5)
        resp.raise_for_status()

        # We wrap it with our timestamp to track sending time
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "raw_forecast": resp.json()
        }

    except Exception as e:
        print("❌ Failed to fetch forecast data:", e)
        return None


def run_forecast_sensor():
    """
    Loop that continuously fetches and sends raw forecast data.
    Ready to be called from main.py using a thread.
    """
    
    print("☁️ Forecast Sensor Started...")
    #print("Gateway URL:", GATEWAY_URL)

    while True:
        payload = fetch_raw_forecast()

        if payload:
            try:
                response = requests.post(GATEWAY_URL, json=payload, timeout=5)
                print("📤 Sent forecast | Gateway:", response.json())
            except Exception as e:
                print("❌ Failed to send forecast data:", e)
        else:
            print("⚠️ Skipping sending due to fetch error.")

        time.sleep(10)  # send every 10 seconds
