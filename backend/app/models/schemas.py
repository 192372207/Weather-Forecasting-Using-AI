from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any

# User Models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    profile_pic: Optional[str] = None
    role: str = "user"
    created_at: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Weather Models
class LocationQuery(BaseModel):
    city: str

class WeatherCurrentResponse(BaseModel):
    city: str
    country: str
    lat: float
    lon: float
    temp: float
    feels_like: float
    humidity: int
    wind_speed: float
    wind_direction: int
    pressure: float
    uv_index: float
    aqi: int
    aqi_description: str
    visibility: float
    condition: str
    icon: str
    sunrise: str
    sunset: str
    rain_probability: int
    high: float
    low: float

class HourlyItem(BaseModel):
    time: str
    temp: float
    condition: str
    icon: str
    pop: int
    wind_speed: float

class DailyItem(BaseModel):
    date: str
    day: str
    condition: str
    icon: str
    high: float
    low: float
    rain_prob: int
    humidity: int
    wind_speed: float

# AI Request/Response
class AIChatRequest(BaseModel):
    message: str
    city: Optional[str] = "London"
    current_temp: Optional[float] = None
    condition: Optional[str] = None
    language: Optional[str] = "en"

class AIChatResponse(BaseModel):
    response: str
    suggestions: List[str]
    risk_level: Optional[str] = "Green"

class AIAdviceRequest(BaseModel):
    category: str
    city: str
    language: Optional[str] = "en"

# Safety Assessment Models
class SafetyAssessRequest(BaseModel):
    city: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    language: Optional[str] = "en"

class EmergencyService(BaseModel):
    id: str
    name: str
    category: str  # Hospital, Police, Shelter, Fire
    distance_km: float
    phone: str
    address: str
    lat: float
    lon: float

class SafetyAssessmentResponse(BaseModel):
    city: str
    risk_level: str  # Green, Yellow, Orange, Red
    risk_title: str
    risk_score: int  # 0 to 100
    daily_summary: str
    precautions: List[str]
    health_advice: Dict[str, Any]
    travel_advice: str
    clothing_advice: str
    hazard_warnings: List[Dict[str, str]]
    emergency_services: List[EmergencyService]

# Community Models
class CommunityReportCreate(BaseModel):
    event_type: str
    city: str
    description: str
    image_url: Optional[str] = None

class CommunityReportResponse(BaseModel):
    id: str
    user_name: str
    user_avatar: str
    event_type: str
    city: str
    description: str
    image_url: Optional[str] = None
    likes: int
    comments_count: int
    timestamp: str

# Favorites
class FavoriteCityCreate(BaseModel):
    city: str
    lat: float
    lon: float
    country: Optional[str] = ""

class FavoriteCityResponse(BaseModel):
    id: str
    city: str
    country: str
    lat: float
    lon: float
    temp: float
    condition: str
    icon: str
