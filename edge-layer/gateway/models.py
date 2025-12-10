from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# -----------------------------
# WEATHER (CURRENT)
# -----------------------------
class Coord(BaseModel):
    lon: float
    lat: float


class WeatherItem(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class MainData(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None


class Wind(BaseModel):
    speed: float
    deg: int
    gust: Optional[float] = None


class Clouds(BaseModel):
    all: int


class Sys(BaseModel):
    country: str
    sunrise: int
    sunset: int


class WeatherResponse(BaseModel):
    coord: Coord
    weather: List[WeatherItem]
    base: str
    main: MainData
    visibility: int
    wind: Wind
    clouds: Clouds
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int

class CurrentWeather(BaseModel):
    timestamp: datetime
    raw_weather: WeatherResponse


# -----------------------------
# FORECAST
# -----------------------------
class MainForecast(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None
    humidity: int
    temp_kf: float


class SysForecast(BaseModel):
    pod: str  # "d" / "n"


class ForecastEntry(BaseModel):
    dt: int
    main: MainForecast
    weather: List[WeatherItem]
    clouds: Clouds
    wind: Wind
    visibility: int
    pop: float
    sys: SysForecast
    dt_txt: str


class CityInfo(BaseModel):
    id: int
    name: str
    coord: Coord
    country: str
    population: int
    timezone: int
    sunrise: int
    sunset: int


class ForecastResponse(BaseModel):
    cod: str
    message: int
    cnt: int
    list: List[ForecastEntry]
    city: CityInfo
    
class WeatherForecast(BaseModel):
    timestamp: datetime
    raw_forecast: ForecastResponse


# -----------------------------
# SOIL SENSOR
# -----------------------------

class SoilData(BaseModel):
    timestamp: datetime
    data_type: str
    soil_moisture: float
    soil_ph: float
    soil_temp_c: float
