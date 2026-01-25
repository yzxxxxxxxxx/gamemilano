from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
result = supabase.table('events').select('*').execute()
print('Events in DB:')
for e in result.data:
    print(f'{e["event_time"]} - {e["title"]}')