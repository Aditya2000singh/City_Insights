import httpx
from datetime import datetime
from app.models.snapshot import CurrencyData
from app.config import get_settings

settings = get_settings()


async def fetch_currency(currency_code: str) -> CurrencyData | None:
    """
    Fetch exchange rate: 1 unit of currency_code → INR.
    Uses exchangerate-api.com free tier.
    """
    if currency_code == "INR":
        return CurrencyData(
            code="INR",
            rate_to_inr=1.0,
            last_updated=datetime.utcnow(),
        )

    url = f"https://v6.exchangerate-api.com/v6/{settings.exchange_rate_api_key}/pair/{currency_code}/INR"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()

        if data.get("result") != "success":
            raise ValueError(f"API error: {data.get('error-type')}")

        return CurrencyData(
            code=currency_code,
            rate_to_inr=data["conversion_rate"],
            last_updated=datetime.utcnow(),
        )
    except Exception as e:
        print(f"[CurrencyService] Error for {currency_code}: {e}")
        return None
