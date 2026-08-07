from fastapi import APIRouter, Query
from app.services.weather_service import get_current_weather, get_hourly_forecast, get_daily_forecast
from typing import List, Dict, Any

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/current")
async def current_weather(city: str = Query("London", description="City name")):
    return await get_current_weather(city)

@router.get("/hourly")
async def hourly_forecast(city: str = Query("London", description="City name")):
    return await get_hourly_forecast(city)

@router.get("/daily")
async def daily_forecast(city: str = Query("London", description="City name"), days: int = Query(7, ge=1, le=15)):
    return await get_daily_forecast(city, days)

@router.get("/forecast")
async def full_forecast(city: str = Query("London")):
    current = await get_current_weather(city)
    hourly = await get_hourly_forecast(city)
    daily7 = await get_daily_forecast(city, 7)
    daily15 = await get_daily_forecast(city, 15)
    return {
        "current": current,
        "hourly": hourly,
        "daily_7": daily7,
        "daily_15": daily15
    }
