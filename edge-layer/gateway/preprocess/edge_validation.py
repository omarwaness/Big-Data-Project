# edge_validation.py
#   Check fields, types, ranges
#   Reject if invalid ---> aise ValueError("Temperature out of range")

from models import CleanWeather
from models import CleanForecast
from models import SoilData


def validate_weather(data: CleanWeather) -> CleanWeather:
    """
    Validate CleanWeather object.
    Raises ValueError if any value is out of expected range.
    """
    if not (-50 <= data.temp <= 60):
        raise ValueError(f"Temperature out of range: {data.temp}")
    if not (-50 <= data.temp_min <= 60):
        raise ValueError(f"Min temperature out of range: {data.temp_min}")
    if not (-50 <= data.temp_max <= 60):
        raise ValueError(f"Max temperature out of range: {data.temp_max}")
    if not (0 <= data.humidity <= 100):
        raise ValueError(f"Humidity out of range: {data.humidity}")
    if not (0 <= data.pressure <= 2000):
        raise ValueError(f"Pressure out of range: {data.pressure}")
    if not (0 <= data.wind_speed <= 150):
        raise ValueError(f"Wind speed out of range: {data.wind_speed}")

    return data


def validate_forecast(data: CleanForecast) -> CleanForecast:
    """
    Validate CleanForecast object.
    Raises ValueError if any value is out of expected range.
    """
    if len(data.readings) != 10:
        raise ValueError(f"Forecast must have exactly 10 readings, got {len(data.readings)}")

    for i, entry in enumerate(data.readings):
        if not (-50 <= entry.temp <= 60):
            raise ValueError(f"Reading {i} temp out of range: {entry.temp}")
        if not (0 <= entry.humidity <= 100):
            raise ValueError(f"Reading {i} humidity out of range: {entry.humidity}")
        if not (0 <= entry.wind_speed <= 150):
            raise ValueError(f"Reading {i} wind_speed out of range: {entry.wind_speed}")
        if entry.rain < 0:
            raise ValueError(f"Reading {i} rain cannot be negative: {entry.rain}")

    return data




def validate_soil(data: SoilData) -> SoilData:
    """
    Validate SoilData object.
    Raises ValueError if any value is out of realistic range.
    """
    if not (0 <= data.soil_moisture <= 100):
        raise ValueError(f"Soil moisture out of range: {data.soil_moisture}")
    if not (0 <= data.soil_ph <= 14):
        raise ValueError(f"Soil pH out of range: {data.soil_ph}")
    if not (-10 <= data.soil_temp_c <= 50):
        raise ValueError(f"Soil temperature out of realistic range: {data.soil_temp_c}")

    return data

