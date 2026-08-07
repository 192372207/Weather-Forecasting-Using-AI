import datetime
from jose import jwt, JWTError
import hashlib
from app.config import settings
from typing import Dict, Any, Optional

def hash_password(password: str) -> str:
    # Use sha256 with salt for clean cross-platform compatibility
    salt = settings.SECRET_KEY[:16]
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# In-Memory Fallback Data Store for seamless execution without MongoDB setup
DB_STORE: Dict[str, list] = {
    "users": [
        {
            "id": "usr_demo_001",
            "name": "Demo User",
            "email": "demo@skysense.ai",
            "password": hash_password("demo1234"),
            "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=DemoUser",
            "role": "user",
            "created_at": "2026-01-15T10:00:00Z"
        },
        {
            "id": "usr_admin_001",
            "name": "Admin SkySense",
            "email": "admin@skysense.ai",
            "password": hash_password("admin1234"),
            "profile_pic": "https://api.dicebear.com/7.x/avataaars/svg?seed=AdminSkySense",
            "role": "admin",
            "created_at": "2026-01-01T00:00:00Z"
        }
    ],
    "favorites": [
        {
            "id": "fav_001",
            "city": "London",
            "country": "United Kingdom",
            "lat": 51.5074,
            "lon": -0.1278,
            "temp": 19.5,
            "condition": "Partly Cloudy",
            "icon": "cloud-sun"
        },
        {
            "id": "fav_002",
            "city": "Tokyo",
            "country": "Japan",
            "lat": 35.6762,
            "lon": 139.6503,
            "temp": 24.2,
            "condition": "Clear Sky",
            "icon": "sun"
        }
    ],
    "reports": [
        {
            "id": "rep_001",
            "user_name": "Elena Rostova",
            "user_avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Elena",
            "event_type": "Heavy Rain",
            "city": "Paris",
            "description": "Heavy rainfall starting near Eiffel Tower area. Road visibility is reduced to under 500m.",
            "image_url": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?auto=format&fit=crop&w=800&q=80",
            "likes": 14,
            "comments_count": 3,
            "timestamp": "25 mins ago"
        },
        {
            "id": "rep_002",
            "user_name": "Marcus Vance",
            "user_avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=Marcus",
            "event_type": "Storm",
            "city": "Sydney",
            "description": "High winds approaching Darling Harbour with minor thunder activity.",
            "image_url": "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?auto=format&fit=crop&w=800&q=80",
            "likes": 29,
            "comments_count": 8,
            "timestamp": "1 hour ago"
        }
    ]
}
