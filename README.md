# Vagabond — Premium Tourist Discovery Web Application

Vagabond is a modern, enterprise-grade travel exploration web application designed for tourists to discover local attractions dynamically within a specified radius. Built with a luxury travel aesthetic, it provides interactive maps, step-by-step driving route directions, and comprehensive place reviews without requiring login or sign-up.

---

## 🌟 Tech Stack

### Backend
* **Python 3.12** & **FastAPI** (asynchronous controller routing)
* **SQLAlchemy 2.0** (async model ORM) & **PostgreSQL** (persistence)
* **Redis** (search queries and rate-limiting cache)
* **Alembic** (database schema migrations)
* **Pydantic v2** (data schemas and strict input validation)

### Frontend
* **React 19** & **TypeScript** & **Vite** (bundler)
* **Tailwind CSS v4** & **Framer Motion** (luxury fluid styling and custom animations)
* **React Query** (asynchronous query caching & synchronization)
* **Axios** (API requests client)
* **Google Maps JavaScript SDK**

---

## 🚀 Quickstart: Docker Compose (Recommended)

To launch the complete application stack (Frontend, Backend, PostgreSQL database, and Redis cache) with one command, ensure you have Docker installed and run:

```bash
docker-compose up --build
```

* **Frontend Dashboard**: Access `http://localhost` (port 80)
* **Backend API Documentation (Swagger Docs)**: Access `http://localhost:8000/docs`
* **PostgreSQL Database**: Port `5432`
* **Redis Cache**: Port `6379`

---

## 🛠️ Local Development Setup (Manual)

If you prefer to run services individually without Docker:

### 1. Prerequisites
Ensure you have **Python 3.9+** and **Node.js 20+** installed locally.

### 2. Backend Setup
1. Navigate to the backend folder and create a virtual environment:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configure your environment variables. Create a `.env` file inside the `backend/` folder:
   ```env
   DATABASE_URL=sqlite+aiosqlite:///./tourist.db
   REDIS_URL=redis://localhost:6379/0
   USE_REDIS=False
   GOOGLE_MAPS_API_KEY=your_optional_google_api_key
   ```
   *(Setting `USE_REDIS=False` will trigger an automated in-memory cache fallback so a local Redis server isn't strictly required).*
3. Run Alembic migrations to initialize the database:
   ```bash
   alembic upgrade head
   ```
4. Start the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### 3. Frontend Setup
1. Navigate to the frontend folder and install npm dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Configure environment variables in `frontend/.env`:
   ```env
   VITE_API_URL=http://localhost:8000/api/v1
   VITE_GOOGLE_MAPS_API_KEY=your_optional_google_api_key
   ```
3. Start the Vite React development server:
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173` in your browser.

---

## 🗺️ Google Maps Integration & Mock Mode

The application supports two operating modes depending on credentials availability:

### 1. Mock Mode (Default)
If `GOOGLE_MAPS_API_KEY` (in backend) and `VITE_GOOGLE_MAPS_API_KEY` (in frontend) are **empty**, the application operates in **Mock Mode**:
* City queries (like **Paris**, **Rome**, **Tokyo**) will resolve to curated mock coordinates.
* Attractions are fetched from a pre-loaded local dataset featuring actual descriptions, coordinates, ratings, and beautiful Unsplash images.
* Google Map falls back to an interactive, animated vector SVG Radar Dashboard showing live pins and route lines.

### 2. Live Mode
Provide a billing-enabled Google Cloud API Key in both backend and frontend environments to activate the live SDK:
* **Backend Geocoding**: Translates any location string into precise lat/lng.
* **Google Places TextSearch API**: Discovers live tourist attractions within the designated radius.
* **Google Place Details API**: Fetches live operational status, ratings, images, and reviews.
* **Google Directions API**: Computes real-world driving steps and renders the route polyline.

---

## 🛡️ Security Implementations

* **Rate Limiting**: Custom FastAPI middleware throttles requests by client IP (default 60 requests per minute) to prevent server/API billing abuse.
* **Input Sanitization**: Pydantic validates inputs strictly, preventing XSS and injection payloads.
* **SQL Injection Prevention**: SQLAlchemy parameters are fully parameterized at the DB driver layer.
* **Secure Cache Expirations**: Redis cache values expire after 24 hours to automatically evict stale values and keep Places API caching legal under Google Maps terms of use.
