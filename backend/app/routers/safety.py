from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any
from app.models.schemas import SafetyAssessmentResponse, EmergencyService, SafetyAssessRequest
from app.services.weather_service import get_current_weather

router = APIRouter(prefix="/safety", tags=["Safety Assistant & Emergency"])

@router.get("/assess", response_model=SafetyAssessmentResponse)
async def get_safety_assessment(city: str = Query("London"), language: str = Query("en")):
    cur = await get_current_weather(city)
    
    # Calculate Risk Score (0-100) & Level (Green, Yellow, Orange, Red)
    temp = cur["temp"]
    rain_prob = cur["rain_probability"]
    wind = cur["wind_speed"]
    uv = cur["uv_index"]
    aqi = cur["aqi"]
    cond_lower = cur["condition"].lower()

    risk_score = 15
    if "storm" in cond_lower or "cyclone" in cond_lower or wind > 40:
        risk_score += 55
    if "rain" in cond_lower or rain_prob > 60:
        risk_score += 25
    if aqi > 100:
        risk_score += 20
    if uv > 8:
        risk_score += 15
    if temp > 38 or temp < 2:
        risk_score += 25

    risk_score = min(risk_score, 100)

    if risk_score >= 75:
        risk_level = "Red"
        risk_title = "EXTREME DANGER / HAZARD ALERT"
    elif risk_score >= 50:
        risk_level = "Orange"
        risk_title = "HIGH RISK WEATHER"
    elif risk_score >= 30:
        risk_level = "Yellow"
        risk_title = "MODERATE CAUTION REQUIRED"
    else:
        risk_level = "Green"
        risk_title = "SAFE WEATHER CONDITIONS"

    # Precise safety precautions list
    precautions = []
    if rain_prob > 40 or "rain" in cond_lower:
        precautions.append("☔ Carry a durable umbrella and rain poncho.")
        precautions.append("🚗 Avoid flooded roads and waterlogged underpasses.")
    if uv > 6:
        precautions.append("☀️ Apply SPF 30+ sunscreen and wear sunglasses.")
        precautions.append("🕶️ Avoid direct sunlight exposure between 11 AM - 3 PM.")
    if aqi > 70:
        precautions.append("😷 Wear an N95 respiratory mask during outdoor commutes.")
        precautions.append("🪟 Keep indoor windows closed during peak traffic hours.")
    if wind > 20:
        precautions.append("🌬️ Avoid standing under old trees, hoardings, or power lines.")
    if temp > 32:
        precautions.append("💧 Stay hydrated: Drink at least 3 liters of water today.")
    if not precautions:
        precautions.append("✅ Weather conditions are pleasant. Normal outdoor activities safe.")

    # Daily Summary
    daily_summary = (
        f"Today in {cur['city']}: Temp {cur['temp']}°C, Rain Chance {cur['rain_probability']}%, "
        f"Wind {cur['wind_speed']} km/h, AQI {cur['aqi']} ({cur['aqi_description']}). "
        f"Overall risk level is {risk_level}."
    )

    # Nearby emergency services simulation
    emergency_services = [
        EmergencyService(
            id="emg_001",
            name=f"{cur['city']} General Hospital & Emergency",
            category="Hospital",
            distance_km=1.2,
            phone="112",
            address=f"Central Medical Drive, {cur['city']}",
            lat=cur["lat"] + 0.01,
            lon=cur["lon"] + 0.01
        ),
        EmergencyService(
            id="emg_002",
            name=f"{cur['city']} Metropolitan Police Station",
            category="Police",
            distance_km=2.4,
            phone="100",
            address=f"Civic Headquarters, {cur['city']}",
            lat=cur["lat"] - 0.01,
            lon=cur["lon"] - 0.01
        ),
        EmergencyService(
            id="emg_003",
            name=f"{cur['city']} Disaster Relief Shelter",
            category="Shelter",
            distance_km=3.1,
            phone="108",
            address=f"Community Complex, {cur['city']}",
            lat=cur["lat"] + 0.02,
            lon=cur["lon"] - 0.01
        )
    ]

    hazard_warnings = []
    if risk_level in ["Orange", "Red"]:
        hazard_warnings.append({
            "title": f"Active {risk_title} for {cur['city']}",
            "severity": risk_level,
            "instruction": "Follow local authority instructions and keep emergency supplies ready."
        })

    return SafetyAssessmentResponse(
        city=cur["city"],
        risk_level=risk_level,
        risk_title=risk_title,
        risk_score=risk_score,
        daily_summary=daily_summary,
        precautions=precautions,
        health_advice={
            "aqi_advice": f"AQI is {cur['aqi']} ({cur['aqi_description']}). Moderate outdoor exercise safe.",
            "uv_advice": f"UV Index is {cur['uv_index']}. Wear sunscreen if out.",
            "hydration_liters": 2.5 if temp < 30 else 3.5,
            "vulnerable_groups": "Elderly and children should take extra caution during midday heat."
        },
        travel_advice="Driving conditions are safe with clear road visibility.",
        clothing_advice="Wear light, breathable clothes with a light jacket for dusk.",
        hazard_warnings=hazard_warnings,
        emergency_services=emergency_services
    )

@router.get("/emergency-services")
async def get_emergency_services(city: str = "London"):
    cur = await get_current_weather(city)
    return [
        {
            "id": "emg_001",
            "name": f"{cur['city']} Central Emergency Hospital",
            "category": "Hospital",
            "distance": "1.2 km",
            "phone": "112",
            "address": "Medical Square, City Center"
        },
        {
            "id": "emg_002",
            "name": "National Disaster Helpline",
            "category": "Disaster Helpline",
            "distance": "Direct Line",
            "phone": "1078",
            "address": "24/7 Command Center"
        },
        {
            "id": "emg_003",
            "name": f"{cur['city']} Central Police HQ",
            "category": "Police",
            "distance": "2.1 km",
            "phone": "100",
            "address": "Civic Plaza"
        },
        {
            "id": "emg_004",
            "name": f"{cur['city']} Fire & Rescue Services",
            "category": "Fire",
            "distance": "1.8 km",
            "phone": "101",
            "address": "Station 4, Main Ave"
        }
    ]
