from fastapi import APIRouter, HTTPException
from app.models.city import CITIES_MAP
from app.services.weather_service import fetch_weather

router = APIRouter(prefix="/api")


@router.get("/weather/{city_id}")
async def get_weather(city_id: str):
    """
    Fetch live weather for a city on demand.
    Returns JSON — useful for debugging or external consumers.
    """
    city = CITIES_MAP.get(city_id)
    if not city:
        raise HTTPException(status_code=404, detail=f"City '{city_id}' not found.")

    weather = await fetch_weather(city)
    if not weather:
        raise HTTPException(status_code=503, detail="Weather data unavailable right now.")

    return {
        "city_id": city.id,
        "city_name": city.name,
        "temp_c": weather.temp_c,
        "feels_like_c": weather.feels_like_c,
        "humidity": weather.humidity,
        "pressure": weather.pressure,
        "wind_speed": weather.wind_speed,
        "description": weather.description,
        "icon_url": f"https://openweathermap.org/img/wn/{weather.icon}@2x.png",
    }
