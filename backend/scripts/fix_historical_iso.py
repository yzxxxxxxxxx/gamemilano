
import os
import sys
from supabase import create_client

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from backend.config import SUPABASE_URL, SUPABASE_KEY
from backend.scripts.sync_medals import get_iso

# Set proxies
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["NO_PROXY"] = "*"

def fix_historical_iso():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    table = "history_medals_duplicate"
    
    try:
        # Get all records to check their country and current iso
        # Note: Select id as well if exists to update specifically, otherwise use combinations
        # Looking at previous logs, columns are Year, City, Country, Rank, iso, gold, silver, bronze
        res = supabase.table(table).select("*").execute()
        if not res.data:
            print("No data found in history_medals_duplicate")
            return

        print(f"Checking {len(res.data)} records in {table}...")
        
        updates_count = 0
        for row in res.data:
            country = row.get("Country") or row.get("country")
            current_iso = row.get("iso")
            
            if not country:
                continue
                
            correct_iso = get_iso(country)
            
            if correct_iso != current_iso:
                # Update this record
                # We need a way to identify the record uniquely. 
                # Usually Year, Country, Rank should be unique enough for historical medals.
                query = supabase.table(table).update({"iso": correct_iso})
                
                if "Year" in row:
                    query = query.eq("Year", row["Year"])
                if "Country" in row:
                    query = query.eq("Country", row["Country"])
                if "Rank" in row:
                    query = query.eq("Rank", row["Rank"])
                
                try:
                    query.execute()
                    updates_count += 1
                    print(f"Updated: {country} ({current_iso} -> {correct_iso})")
                except Exception as e:
                    print(f"Error updating {country}: {e}")

        print(f"\nSuccessfully updated {updates_count} records.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fix_historical_iso()
