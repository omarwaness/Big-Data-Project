
from models import CleanWeather
from models import CurrentWeather
from models import CleanForecast
from models import WeatherForecast

# extract relavent data only


# function to extract important data from the weather api
def clean_weather(raw: CurrentWeather) -> CleanWeather:
    cleaned = {
        "timestamp": raw.timestamp,
        "description": raw.raw_weather.weather[0].description,

        "temp": raw.raw_weather.main.temp,
        "temp_min": raw.raw_weather.main.temp_min,
        "temp_max": raw.raw_weather.main.temp_max,

        "pressure": raw.raw_weather.main.pressure,
        "humidity": raw.raw_weather.main.humidity,

        "wind_speed": raw.raw_weather.wind.speed,
    }

    return CleanWeather(**cleaned)


# function to extract important data from the forecast api 
def clean_forecast(raw: WeatherForecast) -> CleanForecast:
    cleaned_readings = []

    forecast_list = raw.raw_forecast.list

    for entry in forecast_list[::4][:10]:
        rain_value = entry.rain.h3 if entry.rain is not None else 0.0
        cleaned_entry = {
            "dt_text": entry.dt_txt,
            "description": entry.weather[0].description,

            "temp": entry.main.temp,
            "humidity": entry.main.humidity,
            "wind_speed": entry.wind.speed,
            "rain": rain_value
        }

        cleaned_readings.append(cleaned_entry)

    cleaned = {
        "timestamp": raw.timestamp,
        "readings": cleaned_readings,
    }

    return CleanForecast(**cleaned)

