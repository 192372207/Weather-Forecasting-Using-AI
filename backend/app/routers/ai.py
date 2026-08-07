from fastapi import APIRouter
from app.models.schemas import AIChatRequest, AIChatResponse, AIAdviceRequest
from app.services.ai_service import generate_ai_chat_response, generate_ai_category_advice

router = APIRouter(prefix="/ai", tags=["AI Intelligence"])

@router.post("/chat", response_model=AIChatResponse)
async def ai_chat(payload: AIChatRequest):
    return await generate_ai_chat_response(
        message=payload.message,
        city=payload.city or "London",
        temp=payload.current_temp or 22.0,
        condition=payload.condition or "Clear"
    )

@router.post("/recommendation")
async def ai_recommendation(payload: AIAdviceRequest):
    return await generate_ai_category_advice(payload.category, payload.city)

@router.get("/summary")
async def ai_summary(city: str = "London"):
    advice = await generate_ai_category_advice("clothing", city)
    return {
        "city": city,
        "summary": f"SkySense AI predicts clear skies and comfortable temperatures for {city.title()} today.",
        "quick_tip": advice["advice"]
    }
