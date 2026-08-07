# 🌤️ SkySense AI - Real-Time Weather Forecasting & Intelligence Platform

SkySense AI is a production-style, real-time weather forecasting and intelligence platform inspired by Apple Weather, Tesla Dashboard, and Windy design aesthetics.

---

## 🏗️ Architecture Stack

1. **FastAPI Backend (`backend/`)**:
   - Python FastAPI REST API with Pydantic schemas.
   - Open-Meteo REST API client for real-time weather, AQI, 24-hour hourly & 7/15-day extended forecasts.
   - Groq AI (`llama-3.3-70b-versatile`) integration with intelligent rule-based fallback generator.
   - JWT & Firebase Authentication module.
   - Cloudinary image storage integration & fallback.
   - MongoDB Atlas Motor async driver with in-memory caching store.

2. **React Web Application (`web/`)**:
   - Built with React (Vite) and Tailwind CSS glassmorphism design system.
   - Dynamic ambient glowing backgrounds, light/dark themes, and responsive design.
   - Features:
     - **Landing Page**: Animated weather hero, feature highlights, live weather preview.
     - **Weather Hub (Dashboard)**: Real-time telemetry, 24h hourly forecast carousel, atmospheric metrics grid (Wind, Humidity, Pressure, UV, AQI, Sunrise/Sunset), 7/15 day forecast breakdown.
     - **AI Assistant**: Interactive chat interface with Groq AI intelligence, typing indicators, suggestion pills, markdown formatting.
     - **Interactive Weather Map**: Leaflet map integration with layer controls.
     - **Weather Analytics**: Interactive SVG graphs for Temperature, Precipitation, Wind, and Air Quality.
     - **Community Feed**: Crowd-sourced weather reports with photo attachments & likes.
     - **Multi-City Comparison**: Side-by-side weather telemetry comparison.
     - **Severe Weather Warnings**: Active weather warning alerts.
     - **Admin Panel**: System metrics, user counts, API latency, and log status.

3. **Flutter Android Application (`mobile/`)**:
   - Material 3 design system with glassmorphic cards.
   - Bottom navigation bar: Weather, AI Assistant, Community, and User Profile.
   - Offline fallback caching and location search.

---

## 🚀 Quick Start Guide

### 1. Launch FastAPI Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
* The API interactive documentation will be live at: `http://localhost:8000/docs`

### 2. Launch React Web Application
```bash
cd web
npm install
npm run dev
```
* The web app will launch at: `http://localhost:3000`

### 3. Launch Flutter Mobile App
```bash
cd mobile
flutter pub get
flutter run
```

---

## 🌐 Deployment Guides

### Vercel (Frontend React)
1. Import `web/` repository directory into Vercel.
2. Set Build Command to `npm run build` and Output Directory to `dist`.

### Render (Backend FastAPI)
1. Connect GitHub repository and select `backend/` directory.
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### MongoDB Atlas & Groq Setup
- Add your `MONGODB_URI` and `GROQ_API_KEY` to `backend/.env`.
