from fastapi import APIRouter, HTTPException
from app.models.city import CITIES_MAP
from app.services.aqi_service import fetch_aqi

router = APIRouter(prefix="/api")


@router.get("/aqi/{city_id}")
async def get_aqi(city_id: str):
    """
    Fetch live AQI for a city on demand.
    Returns JSON — useful for debugging or external consumers.
    """
    city = CITIES_MAP.get(city_id)
    if not city:
        raise HTTPException(status_code=404, detail=f"City '{city_id}' not found.")

    aqi = await fetch_aqi(city)
    if not aqi:
        raise HTTPException(status_code=503, detail="AQI data unavailable right now.")

    return {
        "city_id": city.id,
        "city_name": city.name,
        "aqi": aqi.aqi,
        "pm25": aqi.pm25,
        "pm10": aqi.pm10,
        "co": aqi.co,
        "no2": aqi.no2,
        "source": aqi.source,
    }
