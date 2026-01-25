import requests
from datetime import datetime

API_URL = "http://localhost:8000/api/events/featured"

def test_featured_no_date():
    print("Testing Featured (No Date)...")
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            events = response.json()
            print(f"Got {len(events)} events.")
            for e in events:
                china = e.get('is_team_china')
                title = e.get('title', '')
                type_ = e.get('type', '')
                print(f"  - {title} (China: {china}, Type: {type_})")
                
                # Verify Logic
                is_final = type_ == 'final' or '决赛' in title or '金牌' in title
                if not (china or is_final):
                    print(f"    [ERROR] Event does not match criteria!")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}")

def test_featured_with_date():
    # Assume 2026-02-06 has some events based on sample data or logic
    date_str = "2026-02-06"
    print(f"\nTesting Featured (Date: {date_str})...")
    try:
        response = requests.get(f"{API_URL}?date={date_str}")
        if response.status_code == 200:
            events = response.json()
            print(f"Got {len(events)} events.")
            for e in events:
                time = e.get('event_time', '')
                print(f"  - {e['title']} at {time}")
                if date_str not in time:
                     print(f"    [ERROR] Event date mismatch!")
        else:
             print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_featured_no_date()
    test_featured_with_date()
