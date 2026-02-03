
import os
import sys
import asyncio
import httpx

# Set project root to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.config import BOCHA_API_KEY, ZHIPU_API_KEY
from backend.routers.ai import call_bocha_search, call_glm_api

# Disable proxies
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["NO_PROXY"] = "*"

async def test_bocha_integration():
    print(f"Testing with BOCHA_API_KEY: {BOCHA_API_KEY[:5]}...")
    print(f"Testing with ZHIPU_API_KEY: {ZHIPU_API_KEY[:5]}...")
    
    # Test 1: Search only
    query = "2026年米兰冬奥会 苏翊鸣 的最新状态"
    print(f"\n[Test 1] Testing Bocha Search for: {query}")
    search_context = await call_bocha_search(query)
    if search_context:
        print(f"Search Success! Context preview: {search_context[:200]}...")
    else:
        print("Search Failed or returned empty.")

    # Test 2: Full Integration (Search + GLM)
    print(f"\n[Test 2] Testing Full Integration for: {query}")
    if search_context:
        prompt = f"基于以下背景信息，总结苏翊鸣的最新动态：\n{search_context}"
        result = await call_glm_api(prompt)
        if result:
            print(f"Full Integration Success! AI Response: {result}")
        else:
            print("Full Integration Failed: AI returned no result.")
    else:
        print("Skipping AI test because search failed.")

if __name__ == "__main__":
    asyncio.run(test_bocha_integration())
