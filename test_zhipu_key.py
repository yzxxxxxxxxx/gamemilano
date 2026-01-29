import os
from dotenv import load_dotenv

load_dotenv()

async def test_zhipu():
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        print("Error: ZHIPUAI_API_KEY not found in environment")
        return
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    prompt = "请为准备参加2026年米兰-科尔蒂纳冬奥会的中国运动员 苏炳添 提供一段简短且鼓舞人心的总结（最多1000字）。重点介绍他们的专长和一个有趣的小知识。请使用专业的体育评论员语调，并使用中文回复。"
    
    payload = {
        "model": "glm-4-flash",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": 100
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            print(f"Status: {response.status_code}")
            print(f"Response text: {response.text}")
            if response.status_code == 200:
                data = response.json()
                choices = data.get("choices", [])
                if choices:
                    message = choices[0].get("message", {})
                    content = message.get("content", "").strip()
                    print(f"Response: {content}")
                else:
                    print("No choices in response")
            else:
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_zhipu())
