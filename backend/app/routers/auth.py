from fastapi import APIRouter, HTTPException, Depends, status
from app.models.schemas import UserCreate, UserLogin, TokenResponse, UserResponse
from app.utils.security import hash_password, verify_password, create_access_token, DB_STORE
import uuid
import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=TokenResponse)
async def signup(user: UserCreate):
    for u in DB_STORE["users"]:
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="User email already registered.")
            
    new_user = {
        "id": f"usr_{uuid.uuid4().hex[:8]}",
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
        "profile_pic": f"https://api.dicebear.com/7.x/avataaars/svg?seed={user.name}",
        "role": "user",
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    DB_STORE["users"].append(new_user)
    
    token = create_access_token({"sub": new_user["email"], "id": new_user["id"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse(
            id=new_user["id"],
            name=new_user["name"],
            email=new_user["email"],
            profile_pic=new_user["profile_pic"],
            role=new_user["role"],
            created_at=new_user["created_at"]
        )
    }

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    found = None
    for u in DB_STORE["users"]:
        if u["email"] == credentials.email:
            found = u
            break
            
    if not found or not verify_password(credentials.password, found["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token({"sub": found["email"], "id": found["id"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserResponse(
            id=found["id"],
            name=found["name"],
            email=found["email"],
            profile_pic=found["profile_pic"],
            role=found["role"],
            created_at=found["created_at"]
        )
    }

@router.get("/profile", response_model=UserResponse)
async def get_profile(email: str = "demo@skysense.ai"):
    for u in DB_STORE["users"]:
        if u["email"] == email:
            return UserResponse(
                id=u["id"],
                name=u["name"],
                email=u["email"],
                profile_pic=u["profile_pic"],
                role=u["role"],
                created_at=u["created_at"]
            )
    raise HTTPException(status_code=404, detail="User profile not found.")
