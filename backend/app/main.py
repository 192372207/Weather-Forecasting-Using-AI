from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from app.config import settings
from app.routers import auth, weather, ai, community, favorites, alerts, admin, safety

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="SkySense AI - Real-Time Weather Forecasting & Intelligence Platform API"
)

# CORS Middleware setup for Web & Mobile clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers under /api/v1
api_v1_prefix = "/api/v1"
app.include_router(auth.router, prefix=api_v1_prefix)
app.include_router(weather.router, prefix=api_v1_prefix)
app.include_router(ai.router, prefix=api_v1_prefix)
app.include_router(safety.router, prefix=api_v1_prefix)
app.include_router(community.router, prefix=api_v1_prefix)
app.include_router(favorites.router, prefix=api_v1_prefix)
app.include_router(alerts.router, prefix=api_v1_prefix)
app.include_router(admin.router, prefix=api_v1_prefix)

APK_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "SkySense_AI.apk"))

@app.get("/download/apk", response_class=FileResponse)
@app.get("/SkySense_AI.apk", response_class=FileResponse)
async def download_apk():
    if os.path.exists(APK_PATH):
        return FileResponse(
            path=APK_PATH,
            filename="SkySense_AI.apk",
            media_type="application/vnd.android.package-archive"
        )
    return {"error": "APK file not found"}

@app.get("/")
async def root():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "apk_download_url": "/download/apk",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
