import httpx
from app.models.city import City
from app.models.snapshot import AQIData
from app.config import get_settings

settings = get_settings()
BASE_URL = "https://api.openaq.org/v3/locations"


def _pm25_to_aqi_index(pm25: float) -> int:
    """Convert PM2.5 µg/m³ to WHO AQI index 1-5."""
    if pm25 <= 10:   return 1
    if pm25 <= 20:   return 2
    if pm25 <= 25:   return 3
    if pm25 <= 50:   return 4
    return 5


async def fetch_aqi(city: City) -> AQIData | None:
    headers = {}
    if settings.openaq_api_key:
        headers["X-API-Key"] = settings.openaq_api_key

    # Search nearest station by coordinates
    params = {
        "coordinates": f"{city.lat},{city.lon}",
        "radius": 25000,        # 25 km radius
        "limit": 1,
        "order_by": "distance",
    }
    try:
        async with httpx.AsyncClient(timeout=15, headers=headers) as client:
            # Step 1: find nearest location
            loc_resp = await client.get(BASE_URL, params=params)
            loc_resp.raise_for_status()
            locations = loc_resp.json().get("results", [])

            if not locations:
                return AQIData(source="OpenAQ - no station nearby")

            location_id = locations[0]["id"]

            # Step 2: get latest measurements for that location
            meas_resp = await client.get(
                f"https://api.openaq.org/v3/locations/{location_id}/latest"
            )
            meas_resp.raise_for_status()
            measurements = meas_resp.json().get("results", [])

        pm25 = pm10 = co = no2 = None
        for m in measurements:
            param = m.get("parameter", {}).get("name", "")
            val = m.get("value")
            if param == "pm25":  pm25 = val
            elif param == "pm10": pm10 = val
            elif param == "co":   co   = val
            elif param == "no2":  no2  = val

        aqi_index = _pm25_to_aqi_index(pm25) if pm25 is not None else None

        return AQIData(
            aqi=aqi_index,
            pm25=pm25,
            pm10=pm10,
            co=co,
            no2=no2,
            source="OpenAQ",
        )
    except Exception as e:
        print(f"[AQIService] Error for {city.name}: {e}")
        return None
