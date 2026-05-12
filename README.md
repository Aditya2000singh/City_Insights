# 🌍 Global City Insights Dashboard

> Real-time weather, air quality, and currency dashboard for 10 global cities — built with FastAPI, HTMX, Jinja2, Leaflet.js, and MongoDB Atlas.

---

## ✨ Features

- 🗺️ **Interactive World Map** — Dark-themed Leaflet.js map with custom city markers
- 🌡️ **Live Weather** — Temperature, feels like, humidity, pressure, wind speed, condition icon
- 💨 **Air Quality (AQI)** — PM2.5, PM10, CO, NO₂ with WHO AQI color indicator
- 💱 **Currency vs INR** — Real-time exchange rate for each city's local currency
- 📈 **Historical Trends** — 7-day and 15-day Chart.js graphs for temperature and AQI
- ⚡ **Auto Refresh** — Frontend and backend both poll every 30 seconds
- 📱 **Mobile Responsive** — Works on desktop, tablet, and mobile
- 🗃️ **MongoDB Atlas** — Snapshots stored with TTL index (auto-deletes after 15 days)

---

## 🏙️ Cities Covered

| City | Country | Currency |
|------|---------|----------|
| Mumbai | India | INR |
| New York | USA | USD |
| London | UK | GBP |
| Tokyo | Japan | JPY |
| Dubai | UAE | AED |
| Sydney | Australia | AUD |
| Paris | France | EUR |
| Singapore | Singapore | SGD |
| São Paulo | Brazil | BRL |
| Nairobi | Kenya | KES |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Templating | Jinja2 |
| Frontend Interactivity | HTMX |
| Map | Leaflet.js |
| Charts | Chart.js |
| Database | MongoDB Atlas (Motor async driver) |
| Background Jobs | APScheduler |
| HTTP Client | HTTPX (async) |
| Styling | Custom CSS (dark theme) |

---

## 📡 External APIs Used

| API | Purpose | Free Tier |
|-----|---------|-----------|
| [OpenWeatherMap](https://openweathermap.org/api) | Weather data | 1,000 calls/day |
| [OpenAQ v3](https://explore.openaq.org/) | Air quality / AQI | Free with key |
| [ExchangeRate-API](https://www.exchangerate-api.com/) | Currency vs INR | 1,500 calls/month |
| [MongoDB Atlas](https://cloud.mongodb.com) | Database | 512 MB free forever |

---

## 📁 Project Structure

```
city-insights-dashboard/
│
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Pydantic settings (.env reader)
│   ├── database.py              # Motor async MongoDB client + indexes
│   │
│   ├── api/
│   │   ├── cities.py            # Page + HTMX partial routes
│   │   ├── weather.py           # GET /api/weather/{city_id}
│   │   ├── aqi.py               # GET /api/aqi/{city_id}
│   │   └── currency.py          # GET /api/currency/{city_id}
│   │
│   ├── models/
│   │   ├── city.py              # City model + 10 hardcoded cities
│   │   └── snapshot.py          # CitySnapshot model (weather+AQI+currency)
│   │
│   ├── services/
│   │   ├── weather_service.py   # OpenWeatherMap API client
│   │   ├── aqi_service.py       # OpenAQ API client
│   │   ├── currency_service.py  # ExchangeRate-API client
│   │   └── scheduler.py         # APScheduler: fetches all cities every 30s
│   │
│   ├── templates/
│   │   ├── base.html            # Base layout (CDN links, header, modal shell)
│   │   ├── index.html           # Main map page
│   │   └── partials/
│   │       ├── city_modal.html  # HTMX partial: full city data modal
│   │       ├── city_card.html   # HTMX partial: compact sidebar card
│   │       ├── trend_chart.html # HTMX partial: Chart.js trend graph
│   │       └── toast.html       # HTMX out-of-band toast notification
│   │
│   └── static/
│       ├── css/styles.css       # Full dark theme stylesheet
│       └── js/map.js            # Leaflet init, markers, HTMX triggers
│
├── .env                         # Your secrets (never commit this)
├── .env.example                 # Template for .env (safe to commit)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Architecture

```
Browser
  │
  ├─ GET /                        Jinja2 renders map + sidebar
  ├─ Click marker → HTMX          GET /city/{id}/modal  → city_modal.html
  ├─ Click trend tab → HTMX       GET /city/{id}/trend  → trend_chart.html
  └─ Every 30s → HTMX re-fetch    GET /city/{id}/modal  (auto-refresh)

FastAPI Server
  ├─ APScheduler (every 30s)
  │    ├─ fetch_weather()   → OpenWeatherMap
  │    ├─ fetch_aqi()       → OpenAQ
  │    └─ fetch_currency()  → ExchangeRate-API
  │         └─ store CitySnapshot → MongoDB Atlas
  │
  └─ Route handlers read latest snapshot from MongoDB → render Jinja2 partials
```

---

## 🚀 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/city-insights-dashboard.git
cd city-insights-dashboard
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

Open `.env` and fill in your API keys:

```env
MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=city_insights

OPENWEATHER_API_KEY=your_key_here
OPENAQ_API_KEY=your_key_here
EXCHANGE_RATE_API_KEY=your_key_here
```

### 5. Run the server

```bash
uvicorn app.main:app --reload --port 8000
```

Open [http://localhost:8000](http://localhost:8000)

> ✅ Data starts fetching immediately on startup. Click any city marker after a few seconds to see live data.

---

## 🗄️ MongoDB Atlas Setup (Free)

1. Sign up at [https://cloud.mongodb.com](https://cloud.mongodb.com) — no credit card needed
2. Create a free **M0 cluster**
3. **Database Access** → Add user → set username + password → Role: **Atlas Admin**
4. **Network Access** → Add IP → **Allow from anywhere** (`0.0.0.0/0`)
5. **Database** → Connect → Drivers → Copy connection string → paste into `.env`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main dashboard page |
| `GET` | `/city/{city_id}/modal` | HTMX partial — city modal with live data |
| `GET` | `/city/{city_id}/trend?days=7` | HTMX partial — trend chart (7 or 15 days) |
| `GET` | `/api/weather/{city_id}` | JSON — live weather for a city |
| `GET` | `/api/aqi/{city_id}` | JSON — live AQI for a city |
| `GET` | `/api/currency/{city_id}` | JSON — live currency vs INR |

**Example requests:**
```
GET /api/weather/mumbai
GET /api/aqi/tokyo
GET /api/currency/london
```

---

## 🗃️ MongoDB Schema

**Collection: `snapshots`**

```json
{
  "city_id": "mumbai",
  "fetched_at": "2025-01-01T12:00:00Z",
  "weather": {
    "temp_c": 31.2,
    "feels_like_c": 34.5,
    "humidity": 78,
    "pressure": 1008,
    "wind_speed": 4.2,
    "description": "Scattered Clouds",
    "icon": "03d"
  },
  "aqi": {
    "aqi": 3,
    "pm25": 22.4,
    "pm10": 41.1,
    "co": null,
    "no2": 18.3,
    "source": "OpenAQ"
  },
  "currency": {
    "code": "INR",
    "rate_to_inr": 1.0,
    "last_updated": "2025-01-01T12:00:00Z"
  }
}
```

**Indexes:**
- TTL index on `fetched_at` — auto-deletes documents after 15 days
- Compound index on `(city_id, fetched_at)` — fast trend queries

---

## 👤 Author

**Aditya Singh**
Full-Stack Developer | Python · FastAPI · Django · PostgreSQL

