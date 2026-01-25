from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime

# Load env from backend/.env
load_dotenv('backend/.env')

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("Missing credentials")
    exit(1)

supabase = create_client(url, key)

def test_date(date_str):
    print(f"\n=== Testing Date: {date_str} ===")
    
    # 1. Fetch raw events for the day
    start = f"{date_str}T00:00:00"
    end = f"{date_str}T23:59:59"
    
    print(f"Querying range: {start} to {end}")
    
    try:
        raw = supabase.table("events").select("*").gte("event_time", start).lte("event_time", end).execute()
        print(f"Total events found on this date: {len(raw.data)}")
        
        for e in raw.data:
            print(f"  - [{e['id']}] {e['title']} | China:{e['is_team_china']} | Type:{e['type']} | Discipline:{e['discipline']}")
            
            # Manual check logic
            match_china = e['is_team_china']
            match_type = e['type'] == 'final'
            match_title = '决赛' in e['title'] or '金牌' in e['title']
            match_disc = '决赛' in e['discipline'] or '金牌' in e['discipline']
            
            if match_china or match_type or match_title or match_disc:
                print("    -> SHOULD MATCH!")
            else:
                print("    -> Should NOT match.")

        # 2. Test the OR filter
        print("\nTesting OR Filter query...")
        filter_str = "is_team_china.eq.true,type.eq.final,title.ilike.%决赛%,title.ilike.%金牌%,discipline.ilike.%决赛%,discipline.ilike.%金牌%"
        
        filtered = supabase.table("events").select("*") \
            .gte("event_time", start).lte("event_time", end) \
            .or_(filter_str) \
            .execute()
            
        print(f"Filtered API Result count: {len(filtered.data)}")
        for e in filtered.data:
             print(f"  - MATCHED: {e['title']}")

    except Exception as e:
        print(f"Query failed: {e}")

if __name__ == "__main__":
    test_date("2026-02-04")
    test_date("2026-02-05")
