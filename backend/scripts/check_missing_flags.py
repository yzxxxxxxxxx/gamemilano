
import os
import sys
from supabase import create_client

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from backend.config import SUPABASE_URL, SUPABASE_KEY
from backend.scripts.sync_medals import COUNTRY_MAP

# Set proxies
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["NO_PROXY"] = "*"

def check_missing_flags():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Try both table names
    tables = ["history_medals_duplicate", "historical_medals"]
    
    all_countries = set()
    for table in tables:
        try:
            res = supabase.table(table).select("Country").execute()
            if res.data:
                print(f"Checking table: {table}")
                for row in res.data:
                    all_countries.add(row["Country"])
        except Exception as e:
            # Maybe the column name is different
            try:
                res = supabase.table(table).select("country").execute()
                if res.data:
                    print(f"Checking table: {table} (lowercase country)")
                    for row in res.data:
                        all_countries.add(row["country"])
            except:
                print(f"Table {table} not found or inaccessible.")

    missing = []
    for country in sorted(list(all_countries)):
        if country not in COUNTRY_MAP:
            missing.append(country)
            
    print("\nCountries missing in COUNTRY_MAP:")
    for country in missing:
        # Check if the fallback get_iso works for it (first 2 chars)
        # Often for Chinese names like 苏联, it results in 苏联 which is not a valid ISO
        iso_fallback = country[:2].upper()
        print(f"  {country} -> fallback ISO: {iso_fallback}")

if __name__ == "__main__":
    check_missing_flags()
