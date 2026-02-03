"""
AI助手API路由
使用httpx直接调用智谱GLM-4.7-Flash REST API
"""
from fastapi import APIRouter
import httpx
from typing import Optional  # 修复返回值类型注解

from backend.config import ZHIPU_API_KEY, BOCHA_API_KEY
from backend.models import AIAthleteRequest, AIEventRequest, AIResponse

router = APIRouter(prefix="/api/ai", tags=["ai"])

# 智谱 AI API 端点 (OpenAI 兼容)
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
# 博查 AI API 端点
BOCHA_API_URL = "https://api.bochaai.com/v1/web-search"


async def call_bocha_search(query: str) -> str:
    """
    调用博查联网搜索 API 获取实时背景信息
    """
    if not BOCHA_API_KEY:
        print("BOCHA_API_KEY is missing!")
        return ""
    
    headers = {
        "Authorization": f"Bearer {BOCHA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query,
        "freshness": "no_limit",
        "summary": True,
        "count": 8
    }
    
    print(f"Calling BOCHA API for: {query}...")
    
    async with httpx.AsyncClient() as client:
        try:
            # 去掉代理，直接连接
            response = await client.post(
                BOCHA_API_URL,
                headers=headers,
                json=payload,
                timeout=20.0
            )
            
            if response.status_code == 200:
                data = response.json()
                # 优先获取 AI 总结结果
                summary = data.get("data", {}).get("summary", "")
                if summary:
                    print(f"BOCHA Search Summary Success: {summary[:50]}...")
                    return summary
                
                # 如果没有 AI 总结，拼接网页片段
                web_pages = data.get("data", {}).get("webPages", {}).get("value", [])
                if web_pages:
                    snippets = "\n".join([f"- {p.get('name')}: {p.get('snippet')}" for p in web_pages[:5]])
                    print(f"BOCHA Search Snippets Success: {len(web_pages)} pages found.")
                    return snippets
            else:
                print(f"BOCHA API Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"BOCHA API Exception: {str(e)}")
            
    return ""


async def call_glm_api(prompt: str) -> Optional[str]:
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
                "content": prompt # 使用原始 prompt，支持换行
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    print(f"Calling ZHIPU API for prompt length: {len(prompt)}...")
    
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
    先通过博查联网搜索实时信息，再由智谱生成总结
    """
    safe_athlete_name = request.athlete_name.strip().replace("\n", "").replace('"', '').replace("'", "")
    
    # 1. 联网搜索相关信息
    search_query = f"2026年米兰冬奥会 中国运动员 {safe_athlete_name} 个人简介 运动成就 最新消息"
    search_context = await call_bocha_search(search_query)
    
    # 2. 构造提示词
    if search_context:
        prompt = f"""你是一名专业的体育评论员。基于以下联网实时搜索到的背景信息，请为准备参加2026年米兰-科尔蒂纳冬奥会的中国运动员 {safe_athlete_name} 提供一段简短且鼓舞人心的总结（最多1000字）。

【联网实时背景信息】：
{search_context}

请结合以上背景信息，重点介绍他们的专长、运动特点、主要成就和近期动态。如果信息不足，请基于通用知识并注明。
请使用专业的体育知识回答，语调积极向上，并使用中文回复。"""
    else:
        prompt = f"""你是一名专业的体育评论员，请为准备参加2026年米兰-科尔蒂纳冬奥会的中国运动员 {safe_athlete_name} 提供一段简短且鼓舞人心的总结（最多1000字）。
重点介绍他们的专长、运动项目、运动成就和运动精神，并使用中文回复。"""
    
    try:
        result = await call_glm_api(prompt)
        if result:
            return AIResponse(success=True, message=result)
        else:
            return AIResponse(success=False, message="AI 助手暂时无法获取该运动员简介，请稍后再试。")
    except Exception as e:
        print(f"Athlete insight error: {e}")
        return AIResponse(success=False, message="AI 助手服务异常，请检查网络。")


@router.post("/event", response_model=AIResponse)
async def get_event_prediction(request: AIEventRequest):
    """
    获取赛事预测
    先通过博查联网搜索实时赛况，再由智谱分析
    """
    safe_event_title = request.event_title.strip().replace("\n", "").replace('"', '').replace("'", "")
    
    # 1. 联网搜索实时赛况和预测
    search_query = f"2026年米兰冬奥会 {safe_event_title} 赛事分析 实力对比 夺金分析"
    search_context = await call_bocha_search(search_query)
    
    # 2. 构造提示词
    if search_context:
        prompt = f"""你是一个专业的赛事预测与分析助手。基于以下联网实时搜索到的最新信息，请预测冬奥会项目 "{safe_event_title}" 的比赛前景和可能的结果。

【联网实时赛况与分析】：
{search_context}

你的风格是专业、分析透彻且客观。请分析各代表队或运动员的优势和短板，并使用“概率更高”、“略显优势”、“胜负难料”等客观表述。
字数控制在1000字以内，请使用中文回复。"""
    else:
        prompt = f"""你是一个专业的赛事预测与分析助手，专注于为用户提供赛事前瞻和关键看点分析。
请预测冬奥会项目 "{safe_event_title}" 的最终比赛结果，分析可能的优势和短板。
字数控制在1000字以内，请使用中文回复。"""
    
    try:
        result = await call_glm_api(prompt)
        if result:
            return AIResponse(success=True, message=result)
        else:
            return AIResponse(success=False, message="AI 助手暂时无法回答，请稍后再试。")
    except Exception as e:
        print(f"Event prediction error: {e}")
        return AIResponse(success=False, message="AI 助手服务异常，请检查网络。")
