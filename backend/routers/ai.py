"""
AI助手API路由
使用httpx直接调用Gemini REST API
"""
from fastapi import APIRouter
import httpx

from backend.config import GEMINI_API_KEY
from backend.models import AIAthleteRequest, AIEventRequest, AIResponse

router = APIRouter(prefix="/api/ai", tags=["ai"])

# Gemini API端点
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent"


async def call_gemini_api(prompt: str) -> str:
    """
    调用Gemini API生成内容
    """
    if not GEMINI_API_KEY:
        return None
    
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 200
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload,
            timeout=30.0
        )
        
        if response.status_code == 200:
            data = response.json()
            # 提取生成的文本
            candidates = data.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    return parts[0].get("text", "")
        
        return None


@router.post("/athlete", response_model=AIResponse)
async def get_athlete_insight(request: AIAthleteRequest):
    """
    获取运动员简介
    使用Gemini AI生成简短的运动员介绍
    """
    prompt = f"""请为准备参加2026年米兰-科尔蒂纳冬奥会的中国运动员 {request.athlete_name} 提供一段简短且鼓舞人心的总结（最多50字）。
重点介绍他们的专长和一个有趣的小知识。
请使用专业的体育评论员语调，并使用中文回复。"""
    
    try:
        result = await call_gemini_api(prompt)
        if result:
            return AIResponse(success=True, message=result)
        else:
            return AIResponse(
                success=True,
                message="龙的精神在冰面上高高飞扬。祝我们的运动员好运！"
            )
    except Exception as e:
        return AIResponse(
            success=True,
            message="龙的精神在冰面上高高飞扬。祝我们的运动员好运！"
        )


@router.post("/event", response_model=AIResponse)
async def get_event_prediction(request: AIEventRequest):
    """
    获取赛事预测
    使用Gemini AI分析赛事技术挑战
    """
    prompt = f"""预测冬奥会项目 "{request.event_title}" 中运动员面临的主要技术挑战。
字数控制在60字以内，请使用中文回复。"""
    
    try:
        result = await call_gemini_api(prompt)
        if result:
            return AIResponse(success=True, message=result)
        else:
            return AIResponse(
                success=True,
                message="在这项极具挑战性的冬季项目中，技术精度和心理韧性将是获胜的关键。"
            )
    except Exception as e:
        return AIResponse(
            success=True,
            message="在这项极具挑战性的冬季项目中，技术精度和心理韧性将是获胜的关键。"
        )
