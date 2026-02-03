"""
AI助手API路由
使用httpx直接调用智谱GLM-4.7-Flash REST API
"""
from fastapi import APIRouter
import httpx
from typing import Optional  # 修复返回值类型注解

from backend.config import ZHIPU_API_KEY
from backend.models import AIAthleteRequest, AIEventRequest, AIResponse

router = APIRouter(prefix="/api/ai", tags=["ai"])

# 智谱 AI API 端点 (OpenAI 兼容)
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"


async def call_glm_api(prompt: str) -> Optional[str]:  # 修正返回值类型（原str实际返回None，类型不匹配）
    """
    调用智谱 GLM-4.7-Flash API 生成内容
    """
    if not ZHIPU_API_KEY:
        print("ZHIPU_API_KEY is missing!")
        return None
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZHIPU_API_KEY}"
    }
    
    # 防护Prompt注入：过滤特殊字符
    safe_prompt = prompt.strip().replace("\n", " ").replace('"', '').replace("'", "").replace("\\", "")
    # 构造请求体
    payload = {
        "model": "glm-4-flash",
        "messages": [
            {
                "role": "user",
                "content": safe_prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    print(f"Calling ZHIPU API for: {safe_prompt[:50]}...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                ZHIPU_API_URL,
                headers=headers,
                json=payload,
                timeout=60.0
            )
            
            if response.status_code == 200:
                data = response.json()
                # 提取生成的文本 (OpenAI 格式)
                choices = data.get("choices", [])
                if choices:
                    message = choices[0].get("message", {})
                    content = message.get("content", "").strip()
                    
                    if content:
                        print(f"ZHIPU API Success: {content[:30]}...")
                        return content
                    else:
                        print("ZHIPU API Error: Empty content in response")
                        # 如果 content 为空，检查是否有其他可用字段
                        reasoning = message.get("reasoning_content", "").strip()
                        if reasoning:
                            print(f"Found reasoning_content instead: {reasoning[:30]}...")
                            return reasoning
            else:
                print(f"ZHIPU API Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"ZHIPU API Exception: {str(e)}")
            import traceback
            traceback.print_exc()
        
        return None


@router.post("/athlete", response_model=AIResponse)
async def get_athlete_insight(request: AIAthleteRequest):
    """
    获取运动员简介
    使用智谱 GLM-4.7-Flash AI生成运动员介绍
    """
    # 防护Prompt注入：过滤用户输入的特殊字符
    safe_athlete_name = request.athlete_name.strip().replace("\n", "").replace('"', '').replace("'", "")
    prompt = f"""请为准备参加2026年米兰-科尔蒂纳冬奥会的中国运动员 {safe_athlete_name} 提供一段简短且鼓舞人心的总结（最多1000字）。
重点介绍他们的专长和一个有趣的小知识。
请使用专业的体育评论员语调，并使用中文回复。"""
    
    try:
        result = await call_glm_api(prompt)
        if result:
            return AIResponse(success=True, message=result)
        else:
            # 修复：失败时success置为False（原逻辑错误，前端可正确识别）
            return AIResponse(
                success=False,
                message="AI 助手暂时无法获取该运动员简介，请稍后再试。"
            )
    except Exception as e:
        print(f"Athlete insight error: {e}")
        return AIResponse(
            success=False,  # 修复：异常时success置为False
            message="AI 助手服务异常，请检查网络。"
        )


@router.post("/event", response_model=AIResponse)
async def get_event_prediction(request: AIEventRequest):
    """
    获取赛事预测
    使用智谱 GLM-4.7-Flash AI分析赛事技术挑战
    """
    # 防护Prompt注入：过滤用户输入的特殊字符
    safe_event_title = request.event_title.strip().replace("\n", "").replace('"', '').replace("'", "")
    prompt = f"""预测冬奥会项目 "{safe_event_title}" 中运动员面临的主要技术挑战。
字数控制在100字以内，请使用中文回复。"""
    
    try:
        result = await call_glm_api(prompt)
        if result:
            return AIResponse(success=True, message=result)
        else:
            # 修复：失败时success置为False
            return AIResponse(
                success=False,
                message="AI 助手暂时无法回答，请稍后再试。"
            )
    except Exception as e:
        print(f"Event prediction error: {e}")
        return AIResponse(
            success=False,  # 修复：异常时success置为False
            message="AI 助手服务异常，请检查网络。"
        )