from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class WeatherData(BaseModel):
    temp_c: float
    feels_like_c: float
    humidity: int
    pressure: int
    wind_speed: float           # m/s
    description: str
    icon: str                   # OpenWeatherMap icon code


class AQIData(BaseModel):
    aqi: Optional[int] = None   # 1-5 scale (WHO)
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    co: Optional[float] = None
    no2: Optional[float] = None
    source: str = "OpenAQ"


class CurrencyData(BaseModel):
    code: str
    rate_to_inr: float          # 1 unit of this currency = X INR
    last_updated: datetime


class CitySnapshot(BaseModel):
    city_id: str
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
    weather: Optional[WeatherData] = None
    aqi: Optional[AQIData] = None
    currency: Optional[CurrencyData] = None
    error: Optional[str] = None  # store any fetch errors


# AQI index → human label + color (WHO standard)
AQI_META = {
    1: {"label": "Good",              "color": "#22c55e", "bg": "#dcfce7"},
    2: {"label": "Fair",              "color": "#86efac", "bg": "#f0fdf4"},
    3: {"label": "Moderate",          "color": "#fbbf24", "bg": "#fef9c3"},
    4: {"label": "Poor",              "color": "#f97316", "bg": "#fff7ed"},
    5: {"label": "Very Poor",         "color": "#ef4444", "bg": "#fef2f2"},
}
