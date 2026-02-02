
import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

# Load env
load_dotenv('backend/.env')
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 禁用全局代理以避免 SSL 错误
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["NO_PROXY"] = "*"

def fix_uk_iso():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Missing credentials")
        return

    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # 1. Fix in historical_medals
    print("Fixing historical_medals...")
    res = supabase.table("historical_medals").update({"iso": "GB"}).eq("country", "英国").execute()
    print(f"Updated {len(res.data)} records in historical_medals")

    # 2. Fix in medals (current standings)
    print("Fixing medals...")
    res = supabase.table("medals").update({"iso": "GB"}).eq("country", "英国").execute()
    print(f"Updated {len(res.data)} records in medals")

if __name__ == "__main__":
    fix_uk_iso()
