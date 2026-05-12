from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import init_db, close_db
from app.services.scheduler import start_scheduler, stop_scheduler
from app.api.cities import router as cities_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()
    await close_db()


app = FastAPI(
    title="Global City Insights",
    description="Real-time weather, AQI, and currency dashboard for 10 global cities.",
    version="1.0.0",
    lifespan=lifespan,
)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Routers
app.include_router(cities_router)
