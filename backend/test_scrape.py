import requests
from bs4 import BeautifulSoup

url = "https://www.olympics.com/zh/milano-cortina-2026/schedule/04-feb"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Check if we can find the schedule container
        schedule_container = soup.find('section', {'data-cy': 'PregamesSchedule'})
        if schedule_container:
            print("Found schedule container!")
            events = schedule_container.find_all('article', {'data-cy': 'Event-Card'})
            print(f"Found {len(events)} events.")
        else:
            print("Schedule container NOT found. Content might be dynamic.")
            # Print a bit of body to see what we got
            print(soup.body.text[:200])
    else:
        print("Failed to retrieve page")
except Exception as e:
    print(f"Error: {e}")
