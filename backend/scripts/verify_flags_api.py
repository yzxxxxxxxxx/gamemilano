
import os
import sys
import asyncio

# Set proxies to avoid SSL issues in some environments
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["NO_PROXY"] = "*"

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from backend.routers.medals import get_history_by_year

async def verify_history_api():
    print("Verifying historical API flag mapping...")
    
    # Test cases: Year and a country expected in that year
    test_cases = [
        (1988, "德意志民主共和国"), # East Germany -> GDR
        (1988, "德意志联邦共和国"), # West Germany -> FRG
        (1992, "独立国家联合体"),   # Unified Team -> EUN
        (2022, "苏联", False),      # Soviet Union (Testing if it works if it were there)
        (2018, "俄罗斯奥林匹克运动员"), # OAR -> OAR
        (2022, "丹麦")               # Denmark -> DK
    ]
    
    # Let's check some real years
    years_to_check = [2022, 2018, 1992, 1988]
    
    for year in years_to_check:
        print(f"\n--- Year: {year} ---")
        try:
            medals = await get_history_by_year(year)
            found_test_countries = False
            for m in medals:
                country = m.country
                iso = m.iso
                # Simple check: if iso is character-based (not Chinese chars) and not first 2 chars fallback logic failing
                # Before our change, "苏联" would be "苏联", "丹麦" would be "丹麦"
                
                # Print any interesting ones
                if any(tc[0] == year and tc[1] == country for tc in test_cases) or len(iso) > 3 or any('\u4e00' <= c <= '\u9fff' for c in iso):
                    print(f"  Country: {country:15} | ISO: {iso}")
                    found_test_countries = True
            
            if not found_test_countries:
                print("  (No specific test countries found in this year's data, but checked others)")
        except Exception as e:
            print(f"  Error fetching data for {year}: {e}")

if __name__ == "__main__":
    asyncio.run(verify_history_api())
