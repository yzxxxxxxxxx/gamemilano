
import os
import sys
import asyncio
from supabase import create_client, Client

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from backend.config import SUPABASE_URL, SUPABASE_KEY

# Set proxies
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["NO_PROXY"] = "*"

async def verify_ceremonies():
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    res = supabase.table("events").select("title, type").ilike("title", "%幕式%").execute()
    for row in res.data:
        print(f"Title: {row['title']} | Type: {row['type']}")

if __name__ == "__main__":
    asyncio.run(verify_ceremonies())
