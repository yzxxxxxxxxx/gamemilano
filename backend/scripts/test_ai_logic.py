
import os
import sys
import asyncio
import httpx

# Set root dir - should be the directory containing 'backend' folder
# File is in backend/scripts/test_ai_logic.py, so we need to go up 2 levels to reach e:/AIcoding/gamemilano
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.config import ZHIPU_API_KEY
from backend.routers.ai import call_glm_api

# Set proxies
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["NO_PROXY"] = "*"

async def test_ai_logic():
    print(f"Testing AI logic with ZHIPU_API_KEY: {ZHIPU_API_KEY[:5]}...")
    
    # Test cases
    prompts = [
        "请用一句话介绍苏翊鸣。",
        "北京冬奥会是在哪一年举办的？"
    ]
    
    for prompt in prompts:
        print(f"\nPrompt: {prompt}")
        try:
            result = await call_glm_api(prompt)
            if result:
                print(f"Success! Response: {result}")
            else:
                print("Failed: No result returned from AI.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai_logic())
