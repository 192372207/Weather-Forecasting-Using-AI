import os
from typing import Optional
from app.config import settings

async def upload_image_service(file_bytes: bytes, filename: str) -> str:
    # If Cloudinary credentials are set, attempt Cloudinary upload
    if settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY and settings.CLOUDINARY_API_SECRET:
        try:
            import cloudinary
            import cloudinary.uploader
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET,
                secure=True
            )
            res = cloudinary.uploader.upload(file_bytes, folder="skysense")
            return res.get("secure_url", "")
        except Exception:
            pass
            
    # Mock return image URL for instant out-of-the-box operation
    sample_images = [
        "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1534088568595-a066f410bcda?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1561484930-998b6a7b22e8?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?auto=format&fit=crop&w=800&q=80"
    ]
    idx = len(filename) % len(sample_images)
    return sample_images[idx]
