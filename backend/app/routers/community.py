from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
from app.models.schemas import CommunityReportResponse, CommunityReportCreate
from app.utils.security import DB_STORE
from app.services.cloudinary_service import upload_image_service
import uuid

router = APIRouter(prefix="/community", tags=["Community"])

@router.get("/reports", response_model=List[CommunityReportResponse])
async def list_reports():
    return DB_STORE["reports"]

@router.post("/report", response_model=CommunityReportResponse)
async def create_report(
    event_type: str = Form(...),
    city: str = Form(...),
    description: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    img_url = None
    if image:
        content = await image.read()
        img_url = await upload_image_service(content, image.filename)
    elif not img_url:
        img_url = "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?auto=format&fit=crop&w=800&q=80"
        
    rep = {
        "id": f"rep_{uuid.uuid4().hex[:8]}",
        "user_name": "Community Member",
        "user_avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=UserReporter",
        "event_type": event_type,
        "city": city,
        "description": description,
        "image_url": img_url,
        "likes": 1,
        "comments_count": 0,
        "timestamp": "Just now"
    }
    DB_STORE["reports"].insert(0, rep)
    return rep

@router.post("/reports/{report_id}/like")
async def like_report(report_id: str):
    for r in DB_STORE["reports"]:
        if r["id"] == report_id:
            r["likes"] += 1
            return {"likes": r["likes"]}
    raise HTTPException(status_code=404, detail="Report not found.")
