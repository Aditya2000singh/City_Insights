from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta

from app.models.city import CITIES, CITIES_MAP
from app.models.snapshot import AQI_META
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main map page."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "cities": CITIES,
    })


@router.get("/city/{city_id}/modal", response_class=HTMLResponse)
async def city_modal(request: Request, city_id: str):
    """
    HTMX target: returns the modal partial with live data for a city.
    Called when user clicks a map marker.
    """
    city = CITIES_MAP.get(city_id)
    if not city:
        return HTMLResponse("<p>City not found.</p>", status_code=404)

    db = get_db()
    # Get the most recent snapshot
    snap_doc = await db.snapshots.find_one(
        {"city_id": city_id},
        sort=[("fetched_at", -1)],
    )

    aqi_meta = None
    if snap_doc and snap_doc.get("aqi") and snap_doc["aqi"].get("aqi"):
        aqi_meta = AQI_META.get(snap_doc["aqi"]["aqi"], {})

    return templates.TemplateResponse("partials/city_modal.html", {
        "request": request,
        "city": city,
        "snap": snap_doc,
        "aqi_meta": aqi_meta,
    })


@router.get("/city/{city_id}/trend", response_class=HTMLResponse)
async def city_trend(request: Request, city_id: str, days: int = 7):
    """
    HTMX target: returns the trend chart partial with historical data.
    """
    city = CITIES_MAP.get(city_id)
    if not city:
        return HTMLResponse("<p>City not found.</p>", status_code=404)

    db = get_db()
    since = datetime.utcnow() - timedelta(days=days)
    cursor = db.snapshots.find(
        {"city_id": city_id, "fetched_at": {"$gte": since}},
        sort=[("fetched_at", 1)],
        projection={"fetched_at": 1, "weather.temp_c": 1, "aqi.aqi": 1, "aqi.pm25": 1},
    )
    docs = await cursor.to_list(length=500)

    # Build chart-ready data
    labels = []
    temps = []
    aqis = []
    pm25s = []

    for d in docs:
        labels.append(d["fetched_at"].strftime("%d %b %H:%M"))
        temps.append(d.get("weather", {}).get("temp_c") if d.get("weather") else None)
        aqis.append(d.get("aqi", {}).get("aqi") if d.get("aqi") else None)
        pm25s.append(d.get("aqi", {}).get("pm25") if d.get("aqi") else None)

    return templates.TemplateResponse("partials/trend_chart.html", {
        "request": request,
        "city": city,
        "labels": labels,
        "temps": temps,
        "aqis": aqis,
        "pm25s": pm25s,
        "days": days,
    })
