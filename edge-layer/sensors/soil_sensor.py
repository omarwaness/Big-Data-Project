import os
import time
import random
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("GATEWAY_BASE_URL")
GATEWAY_URL = BASE_URL + "/soil"   # endpoint for soil data


def generate_soil_reading():
    """Generate a realistic simulated soil sensor reading."""

    # Soil moisture realistic: 10% - 60%
    moisture = round(random.uniform(10.0, 60.0), 2)

    # Soil pH realistic for crops: 5.5 - 7.5
    ph = round(random.uniform(5.5, 7.5), 1)

    # Soil temperature realistic: 10°C - 28°C
    temp = round(random.uniform(10.0, 28.0), 1)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "data_type": "SOIL_READING",
        "soil_moisture": moisture,
        "soil_ph": ph,
        "soil_temp_c": temp
    }


def run_soil_sensor():
    """Loop that continuously generates and sends soil readings."""
    
    print("🌱  Soil Sensor Started...")
    #print("Gateway URL:", GATEWAY_URL)

    while True:
        reading = generate_soil_reading()

        try:
            response = requests.post(GATEWAY_URL, json=reading, timeout=5)
            print("📤 Sent soil reading | Gateway status: ", response.status_code)
        except Exception as e:
            print("❌ Failed to send soil data:", e)

        time.sleep(10)  # adjustable interval
