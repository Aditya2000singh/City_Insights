import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.models.city import CITIES
from app.models.snapshot import CitySnapshot
from app.services.weather_service import fetch_weather
from app.services.aqi_service import fetch_aqi
from app.services.currency_service import fetch_currency
from app.database import get_db
from app.config import get_settings

settings = get_settings()
scheduler = AsyncIOScheduler()


async def fetch_and_store_all():
    """Fetch weather, AQI, currency for all 10 cities and store in MongoDB."""
    db = get_db()
    print(f"[Scheduler] Fetching all cities at {datetime.utcnow().isoformat()}")

    tasks = [_fetch_city(city) for city in CITIES]
    snapshots = await asyncio.gather(*tasks, return_exceptions=True)

    docs = []
    for snap in snapshots:
        if isinstance(snap, CitySnapshot):
            docs.append(snap.model_dump())

    if docs:
        await db.snapshots.insert_many(docs)
        print(f"[Scheduler] Stored {len(docs)} snapshots.")


async def _fetch_city(city) -> CitySnapshot:
    weather, aqi, currency = await asyncio.gather(
        fetch_weather(city),
        fetch_aqi(city),
        fetch_currency(city.currency_code),
        return_exceptions=True,
    )
    return CitySnapshot(
        city_id=city.id,
        weather=weather if not isinstance(weather, Exception) else None,
        aqi=aqi if not isinstance(aqi, Exception) else None,
        currency=currency if not isinstance(currency, Exception) else None,
    )


def start_scheduler():
    scheduler.add_job(
        fetch_and_store_all,
        trigger=IntervalTrigger(seconds=settings.poll_interval_seconds),
        id="fetch_cities",
        replace_existing=True,
        next_run_time=datetime.utcnow(),   # run immediately on startup
    )
    scheduler.start()
    print(f"[Scheduler] Started. Polling every {settings.poll_interval_seconds}s.")


def stop_scheduler():
    scheduler.shutdown(wait=False)
    print("[Scheduler] Stopped.")
