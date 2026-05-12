from fastapi import APIRouter, HTTPException
from app.models.city import CITIES_MAP
from app.services.currency_service import fetch_currency

router = APIRouter(prefix="/api")


@router.get("/currency/{city_id}")
async def get_currency(city_id: str):
    """
    Fetch live exchange rate (city currency → INR) for a city.
    Returns JSON — useful for debugging or external consumers.
    """
    city = CITIES_MAP.get(city_id)
    if not city:
        raise HTTPException(status_code=404, detail=f"City '{city_id}' not found.")

    currency = await fetch_currency(city.currency_code)
    if not currency:
        raise HTTPException(status_code=503, detail="Currency data unavailable right now.")

    return {
        "city_id": city.id,
        "city_name": city.name,
        "currency_code": currency.code,
        "currency_name": city.currency_name,
        "rate_to_inr": currency.rate_to_inr,
        "last_updated": currency.last_updated.isoformat(),
    }
