
import asyncio
import sys
import os
import requests
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def test_medals():
    print("\n[Testing Medals Reset]")
    try:
        r = requests.get(f"{BASE_URL}/medals/china")
        data = r.json()
        print(f"China Medals: {data}")
        if data['gold'] == 0 and data['silver'] == 0 and data['bronze'] == 0:
            print("✅ Medals verified as 0.")
        else:
            print("❌ Medals NOT 0. Reset might have failed.")
    except Exception as e:
        print(f"❌ Failed to test medals: {e}")

def test_events_featured():
    print("\n[Testing Featured Events]")
    try:
        r = requests.get(f"{BASE_URL}/events/featured?limit=5")
        data = r.json()
        print(f"Fetched {len(data)} featured events.")
        for e in data:
            print(f"- {e['title']} (China: {e['is_team_china']}, Type: {e['type']})")
        
        # Verify filtering logic roughly (can't strict test without db state knowledge, but checks response format)
        if len(data) > 0:
            print("✅ Featured events API returning data.")
        else:
            print("⚠️ No featured events found (maybe no future events in DB?).")
            
    except Exception as e:
        print(f"❌ Failed to test featured events: {e}")

def test_events_date():
    print("\n[Testing Event Date Filtering]")
    try:
        # Test a specific date, e.g., 2026-02-06
        test_date = "2026-02-06"
        r = requests.get(f"{BASE_URL}/events?event_date={test_date}")
        data = r.json()
        print(f"Events on {test_date}: {len(data)}")
        if len(data) > 0:
            sample = data[0]
            print(f"Sample: {sample['title']} at {sample['event_time']}")
            if test_date in sample['event_time']:
                print("✅ Date filtering works.")
            else:
                print("⚠️ Date filtering returned event with mismatch date (timezone difference possible).")
        else:
             print("⚠️ No events found on test date.")
             
    except Exception as e:
        print(f"❌ Failed to test event date: {e}")

if __name__ == "__main__":
    print("Starting Verification...")
    test_medals()
    test_events_featured()
    test_events_date()
