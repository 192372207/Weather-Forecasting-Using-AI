from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import FavoriteCityCreate, FavoriteCityResponse
from app.utils.security import DB_STORE
from app.services.weather_service import get_current_weather
import uuid

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.get("", response_model=List[FavoriteCityResponse])
async def get_favorites():
    # Update current temps for saved cities dynamically
    updated = []
    for item in DB_STORE["favorites"]:
        try:
            cur = await get_current_weather(item["city"])
            item["temp"] = cur["temp"]
            item["condition"] = cur["condition"]
            item["icon"] = cur["icon"]
        except Exception:
            pass
        updated.append(item)
    return updated

@router.post("", response_model=FavoriteCityResponse)
async def add_favorite(payload: FavoriteCityCreate):
    for f in DB_STORE["favorites"]:
        if f["city"].lower() == payload.city.lower():
            return f
            
    cur = await get_current_weather(payload.city)
    fav = {
        "id": f"fav_{uuid.uuid4().hex[:8]}",
        "city": cur["city"],
        "country": cur["country"],
        "lat": cur["lat"],
        "lon": cur["lon"],
        "temp": cur["temp"],
        "condition": cur["condition"],
        "icon": cur["icon"]
    }
    DB_STORE["favorites"].append(fav)
    return fav

@router.delete("/{favorite_id}")
async def remove_favorite(favorite_id: str):
    DB_STORE["favorites"] = [f for f in DB_STORE["favorites"] if f["id"] != favorite_id]
    return {"message": "Favorite location removed"}
