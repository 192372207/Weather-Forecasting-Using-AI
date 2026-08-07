from fastapi import APIRouter
from app.services.weather_service import get_current_weather
from typing import List, Dict, Any

router = APIRouter(prefix="/alerts", tags=["Severe Weather Alerts"])

@router.get("")
async def get_active_alerts(city: str = "London") -> List[Dict[str, Any]]:
    cur = await get_current_weather(city)
    alerts = []
    
    # Dynamic alert evaluation
    if cur["rain_probability"] > 60:
        alerts.append({
            "id": "alt_001",
            "type": "Heavy Rain Alert",
            "severity": "Warning",
            "city": cur["city"],
            "title": f"Heavy Precipitation Expected in {cur['city']}",
            "description": f"Rain chance is high ({cur['rain_probability']}%). Expect wet roadways and water accumulation.",
            "issued_at": "10 mins ago"
        })
        
    if cur["wind_speed"] > 25:
        alerts.append({
            "id": "alt_002",
            "type": "Storm Alert",
            "severity": "Watch",
            "city": cur["city"],
            "title": f"High Wind Warning ({cur['wind_speed']} km/h)",
            "description": "Strong gusting winds detected. Secure loose outdoor belongings.",
            "issued_at": "1 hour ago"
        })

    if cur["temp"] > 32:
        alerts.append({
            "id": "alt_003",
            "type": "Heatwave Alert",
            "severity": "Caution",
            "city": cur["city"],
            "title": f"Extreme Heat Warning ({cur['temp']}°C)",
            "description": "High temperature notice. Stay hydrated and limit direct midday sun exposure.",
            "issued_at": "30 mins ago"
        })

    if not alerts:
        alerts.append({
            "id": "alt_normal",
            "type": "Advisory",
            "severity": "Info",
            "city": cur["city"],
            "title": f"Normal Weather Conditions for {cur['city']}",
            "description": f"No severe storm, flood, or cyclone warnings currently active for {cur['city']}.",
            "issued_at": "Live"
        })

    return alerts
