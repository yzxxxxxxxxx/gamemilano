
import os
import sys
from datetime import datetime
from supabase import create_client, Client

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# 禁用全局代理以避免 SSL 错误
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["NO_PROXY"] = "*"
os.environ["PYTHONHTTPSVERIFY"] = "0" # Disable SSL verify for some libs

from backend.config import SUPABASE_URL, SUPABASE_KEY

def insert_ceremonies():
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    ceremonies = [
        {
            "sport": "仪式",
            "discipline": "仪式",
            "title": "2026米兰-科尔蒂纳冬奥会：开幕式",
            "event_time": "2026-02-06T20:00:00", # Local Italy time
            "location": "圣西罗体育场",
            "is_team_china": True, # Mark as true so it appears in featured/countdown
            "type": "final"
        },
        {
            "sport": "仪式",
            "discipline": "仪式",
            "title": "2026米兰-科尔蒂纳冬奥会：闭幕式",
            "event_time": "2026-02-22T20:00:00", # Local Italy time
            "location": "维罗纳圆形竞技场",
            "is_team_china": True,
            "type": "final"
        }
    ]
    
    for ceremony in ceremonies:
        try:
            # Check if exists
            res = supabase.table("events").select("id").eq("title", ceremony["title"]).execute()
            if res.data:
                print(f"Update: {ceremony['title']}")
                supabase.table("events").update(ceremony).eq("title", ceremony["title"]).execute()
            else:
                print(f"Insert: {ceremony['title']}")
                supabase.table("events").insert(ceremony).execute()
        except Exception as e:
            print(f"Error processing {ceremony['title']}: {e}")

if __name__ == "__main__":
    insert_ceremonies()
