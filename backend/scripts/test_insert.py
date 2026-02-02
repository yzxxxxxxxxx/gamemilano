
import os
import sys
from supabase import create_client

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from backend.config import SUPABASE_URL, SUPABASE_KEY

# Set proxies
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["NO_PROXY"] = "*"

def test_insert():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    data = {
        "sport": "Test",
        "discipline": "Test",
        "title": "Test Event",
        "event_time": "2026-02-06T12:00:00+00:00",
        "location": "Test Location",
        "type": "preliminary"
    }
    try:
        res = supabase.table("events").insert(data).execute()
        print("Success:", res.data)
    except Exception as e:
        print("Fail:", e)

if __name__ == "__main__":
    test_insert()
