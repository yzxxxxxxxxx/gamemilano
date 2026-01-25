import os
import sys
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from supabase import create_client, Client

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Initialize Supabase client
supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

TARGET_URL = "https://www.olympics.com/zh/milano-cortina-2026/schedule/04-feb"
DATE_STR = "2026-02-04"  # Hardcoded for this specific URL context, can be dynamic later

def scrape_and_update():
    print(f"Starting scrape for {TARGET_URL}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # The schedule is comprised of multiple sections or groups.
    # Based on analysis, we look for the main schedule container.
    # If the specific container ID changes, we might default to listing all 'article' cards.
    
    events_found = 0
    events_inserted = 0
    
    # Attempt to find all event cards directly
    event_cards = soup.find_all('article', {'data-cy': 'Event-Card'})
    print(f"Found {len(event_cards)} event cards.")

    for card in event_cards:
        try:
            # 1. Extract Sport
            # The sport is usually in a header preceding the card, but sometimes inside.
            # Let's look for a preceding header if not inside.
            # DOM analysis showed h2 headers for sports.
            # We can traverse up to find the closest previous h2 or section header.
            # However, simpler if we find the grouping container.
            
            # Strategy: The structure often is:
            # Section -> H2 (Sport) -> Div (Grid) -> Articles (Events)
            # OR
            # List -> Item -> H2 (Sport) + Wrapper -> Articles
            
            # Let's try to infer sport from the card's context or content if possible.
            # If the card doesn't have sport info, we need the section header.
            
            sport_name = "Unknown Sport"
            # Traverse parents to find a container with a sport title?
            # Or simplified: The analysis showed h2[data-cy="text-module"] for Sport Name
            
            # Let's try finding the preceding h2
            parent_section = card.find_parent('div', class_=lambda x: x and 'styles__SportWrapper' in x) # Hypothetical, relying on structure analysis
            if not parent_section:
                 # Fallback: find any previous h2 in the DOM flow
                 curr = card
                 while curr:
                     curr = curr.previous_element
                     if curr and curr.name == 'h2':
                         sport_name = curr.get_text(strip=True)
                         break
            
            # 2. Extract Time
            time_span = card.find('span', {'data-cy': lambda x: x and 'time-container' in x})
            if not time_span:
                # Fallback to fuzzy text match if selector fails
                for span in card.find_all('span'):
                    if ':' in span.text and len(span.text) <= 5: # HH:MM
                        time_span = span
                        break
            
            start_time_str = time_span.get_text(strip=True) if time_span else "00:00"
            
            # 3. Extract Title
            # Usually the main bold text
            title_el = card.find('span', {'data-cy': 'text-module'})
            # If there are multiple, the first might be status or time, so be careful.
            # The title is usually the longest text or has a specific class.
            
            # Analysis says: span[data-cy="text-module"] inside the article.
            # Let's get all text modules
            text_modules = card.find_all('span', {'data-cy': 'text-module'})
            # Usually: [Time, Title, Location] or [Title, Location]
            
            event_title = "Unknown Event"
            location = "Unknown Location"
            
            potential_texts = [t.get_text(strip=True) for t in text_modules if t.get_text(strip=True) != start_time_str]
            
            if len(potential_texts) > 0:
                event_title = potential_texts[0]
            if len(potential_texts) > 1:
                location = potential_texts[1]
                
            # Refine location using finding 'venues' link if possible
            venue_link = card.find('a', href=lambda x: x and '/venues/' in x)
            if venue_link:
                location = venue_link.get_text(strip=True)

            # 4. Check for Medal Event
            # Look for medal icon SVG
            is_medal = False
            if card.find('svg', {'aria-label': lambda x: x and 'Medal' in str(x)}) or \
               card.find(class_=lambda x: x and 'medal' in str(x).lower()):
                is_medal = True
            
            type_val = "medal" if is_medal else "preliminary"
            # "final" is hard to distinguish from "medal" without text parsing, 
            # but usually medal events ARE finals.
            if "决赛" in event_title:
                type_val = "final"

            # 5. Construct timestamp
            # Combine DATE_STR and start_time_str
            # start_time_str might be "19:05"
            try:
                dt_str = f"{DATE_STR} {start_time_str}"
                event_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
                # Add timezone? Assuming local time (CET is UTC+1/UTC+2).
                # For simplicity, we store naive or assume UTC for now, or add offset.
                # Project uses 'TIMESTAMP WITH TIME ZONE', so let's add minimal TZ info or leave naive (defaults to UTC usually in some drivers)
                # But let's use isoformat
                event_time_iso = event_dt.isoformat()
            except ValueError:
                event_time_iso = datetime.now().isoformat() # Fallback

            # 6. Team China Logic
            # Simple keyword match
            is_team_china = "中国" in event_title or "CHN" in event_title

            print(f"Processing: [{start_time_str}] {sport_name} - {event_title} ({type_val})")

            # 7. Insert into Supabase
            data = {
                "sport": sport_name,
                "discipline": sport_name, # Often same as sport in this scraping level
                "title": event_title,
                "event_time": event_time_iso,
                "location": location,
                "is_team_china": is_team_china,
                "type": type_val
            }
            
            # We want to avoid duplicates.
            # We can check if exists, or use upsert if we have a unique constraint.
            # The table has ID as PK.
            # Let's check first.
            
            # Simple check: same title and approximate time?
            # For this scraper, let's just insert.
            # Or better: select by title and sport and day.
            
            existing = supabase.table("events").select("id").eq("title", event_title).eq("sport", sport_name).execute()
            
            if existing.data:
                # Update?
                print(f"  -> Event already exists: {existing.data[0]['id']}")
                # Optional: update
            else:
                res = supabase.table("events").insert(data).execute()
                if res.data:
                    events_inserted += 1
                    print(f"  -> Inserted: {res.data[0]['id']}")
            
            events_found += 1

        except Exception as e:
            print(f"Error processing card: {e}")
            continue

    print(f"\nScrape complete. Found {events_found} events. Inserted {events_inserted} new events.")

if __name__ == "__main__":
    scrape_and_update()