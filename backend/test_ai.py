import httpx
import asyncio
import sys

async def test_ai():
    url_athlete = "http://localhost:8000/api/ai/athlete"
    url_event = "http://localhost:8000/api/ai/event"
    
    async with httpx.AsyncClient() as client:
        print("Testing Athlete Insight...")
        try:
            resp = await client.post(url_athlete, json={"athlete_name": "苏炳添"}, timeout=30.0)
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.json()}")
        except Exception as e:
            print(f"Error testing athlete: {e}")

        print("\nTesting Event Prediction...")
        try:
            resp = await client.post(url_event, json={"event_title": "单板滑雪男子大跳台"}, timeout=30.0)
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.json()}")
        except Exception as e:
            print(f"Error testing event: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai())
