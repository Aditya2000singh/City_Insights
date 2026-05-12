import httpx
from app.models.city import City
from app.models.snapshot import WeatherData
from app.config import get_settings

settings = get_settings()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_weather(city: City) -> WeatherData | None:
    params = {
        "lat": city.lat,
        "lon": city.lon,
        "appid": settings.openweather_api_key,
        "units": "metric",
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(BASE_URL, params=params)
            resp.raise_for_status()
            data = resp.json()

        return WeatherData(
            temp_c=data["main"]["temp"],
            feels_like_c=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            wind_speed=data["wind"]["speed"],
            description=data["weather"][0]["description"].title(),
            icon=data["weather"][0]["icon"],
        )
    except Exception as e:
        print(f"[WeatherService] Error for {city.name}: {e}")
        return None
