"""
测试智谱 GLM-4.7-Flash API 调用
"""
import asyncio
import httpx
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"


async def test_glm_api():
    """测试 GLM API 调用"""
    print(f"API Key 前10位: {ZHIPU_API_KEY[:10] if ZHIPU_API_KEY else 'EMPTY'}")
    print(f"API Key 长度: {len(ZHIPU_API_KEY)}")
    
    if not ZHIPU_API_KEY:
        print("错误: ZHIPU_API_KEY 未设置!")
        return
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZHIPU_API_KEY}"
    }
    
    payload = {
        "model": "glm-4.7-flash",
        "messages": [
            {
                "role": "user",
                "content": "你好，请用一句话介绍你自己。"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 200
    }
    
    print(f"\n请求 URL: {ZHIPU_API_URL}")
    print(f"请求 Model: {payload['model']}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                ZHIPU_API_URL,
                headers=headers,
                json=payload,
                timeout=30.0
            )
            
            print(f"\n响应状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                choices = data.get("choices", [])
                if choices:
                    message = choices[0].get("message", {})
                    content = message.get("content", "").strip()
                    print(f"\n✅ 成功! AI 回复: {content}")
            else:
                print(f"\n❌ 失败! 状态码: {response.status_code}")
                
        except httpx.ConnectError as e:
            print(f"\n❌ 连接错误: {str(e)}")
            print("可能的原因: 网络不通、代理设置问题、防火墙阻止等")
            import traceback
            traceback.print_exc()
        except httpx.TimeoutException as e:
            print(f"\n❌ 超时: {str(e)}")
        except Exception as e:
            print(f"\n❌ 异常: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_glm_api())
