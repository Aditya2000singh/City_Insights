from pydantic import BaseModel
from typing import Optional


class City(BaseModel):
    id: str                  # e.g. "mumbai"
    name: str                # e.g. "Mumbai"
    country: str             # e.g. "India"
    lat: float
    lon: float
    currency_code: str       # e.g. "INR"
    currency_name: str       # e.g. "Indian Rupee"
    timezone: str            # e.g. "Asia/Kolkata"
    openaq_location: str     # OpenAQ location name for AQI lookup


# The 10 hardcoded cities
CITIES: list[City] = [
    City(id="mumbai",      name="Mumbai",       country="India",          lat=19.0760,  lon=72.8777,  currency_code="INR", currency_name="Indian Rupee",      timezone="Asia/Kolkata",      openaq_location="Mumbai"),
    City(id="new_york",    name="New York",      country="USA",            lat=40.7128,  lon=-74.0060, currency_code="USD", currency_name="US Dollar",         timezone="America/New_York",  openaq_location="New York"),
    City(id="london",      name="London",        country="UK",             lat=51.5074,  lon=-0.1278,  currency_code="GBP", currency_name="British Pound",     timezone="Europe/London",     openaq_location="London"),
    City(id="tokyo",       name="Tokyo",         country="Japan",          lat=35.6762,  lon=139.6503, currency_code="JPY", currency_name="Japanese Yen",      timezone="Asia/Tokyo",        openaq_location="Tokyo"),
    City(id="dubai",       name="Dubai",         country="UAE",            lat=25.2048,  lon=55.2708,  currency_code="AED", currency_name="UAE Dirham",        timezone="Asia/Dubai",        openaq_location="Dubai"),
    City(id="sydney",      name="Sydney",        country="Australia",      lat=-33.8688, lon=151.2093, currency_code="AUD", currency_name="Australian Dollar", timezone="Australia/Sydney",  openaq_location="Sydney"),
    City(id="paris",       name="Paris",         country="France",         lat=48.8566,  lon=2.3522,   currency_code="EUR", currency_name="Euro",              timezone="Europe/Paris",      openaq_location="Paris"),
    City(id="singapore",   name="Singapore",     country="Singapore",      lat=1.3521,   lon=103.8198, currency_code="SGD", currency_name="Singapore Dollar",  timezone="Asia/Singapore",    openaq_location="Singapore"),
    City(id="sao_paulo",   name="São Paulo",     country="Brazil",         lat=-23.5505, lon=-46.6333, currency_code="BRL", currency_name="Brazilian Real",    timezone="America/Sao_Paulo", openaq_location="São Paulo"),
    City(id="nairobi",     name="Nairobi",       country="Kenya",          lat=-1.2921,  lon=36.8219,  currency_code="KES", currency_name="Kenyan Shilling",   timezone="Africa/Nairobi",    openaq_location="Nairobi"),
]

CITIES_MAP: dict[str, City] = {c.id: c for c in CITIES}
