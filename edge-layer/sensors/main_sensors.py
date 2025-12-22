import threading
from time import sleep
from weather_sensor import run_weather_sensor
from forecast_sensor import run_forecast_sensor
from soil_sensor import run_soil_sensor


def main():
    print("🚀 Starting all sensors...\n")
    sleep(5)

    threading.Thread(target=run_weather_sensor, daemon=True).start()
    threading.Thread(target=run_forecast_sensor, daemon=True).start()
    threading.Thread(target=run_soil_sensor, daemon=True).start()

    while True:
        pass


if __name__ == "__main__":
    main()