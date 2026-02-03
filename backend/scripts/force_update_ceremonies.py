
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

async def force_update_ceremonies():
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Get the records first to get their IDs
    res = supabase.table("events").select("id, title").ilike("title", "%幕式%").execute()
    records = res.data
    print(f"Found records: {records}")
    
    for record in records:
        print(f"Updating record {record['id']} ({record['title']})...")
        update_res = supabase.table("events").update({"type": "preliminary"}).eq("id", record["id"]).execute()
        print(f"Result: {update_res.data}")

if __name__ == "__main__":
    asyncio.run(force_update_ceremonies())
