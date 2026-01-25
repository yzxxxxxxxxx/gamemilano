
import asyncio
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

async def reset_medals():
    print("Connecting to Supabase...")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("Resetting all medal counts to 0...")
    
    # Update directly
    # Note: supabase-py client `update` affects rows matching filters.
    # To update all, we might need a condition that matches all, e.g. id is not null
    # But for safety, let's list them first or just assume we can update all
    
    # Try updating where gold >= 0 (which should be all)
    data = {"gold": 0, "silver": 0, "bronze": 0}
    
    try:
        # Assuming 'id' > '0' or similar works for "all", otherwise fetch all IDs first
        # It's safer to fetch all and update, or use a broad filter.
        # Let's try fetching all first to be safe and clear.
        response = supabase.table("medals").select("id").execute()
        all_ids = [row['id'] for row in response.data]
        
        print(f"Found {len(all_ids)} medal entries. Updating...")
        
        for mid in all_ids:
             supabase.table("medals").update(data).eq("id", mid).execute()
             
        print("Successfully reset all medals to 0.")
        
    except Exception as e:
        print(f"Error resetting medals: {e}")

if __name__ == "__main__":
    asyncio.run(reset_medals())
