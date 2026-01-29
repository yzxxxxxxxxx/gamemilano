import requests
import json

def test_ai_athlete():
    url = "http://localhost:8000/api/ai/athlete"
    payload = {"athlete_name": "苏翊鸣"}
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ai_athlete()
