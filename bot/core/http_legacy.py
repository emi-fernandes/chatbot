import os, requests

BASE = os.getenv("BACKEND_BASE_URL", "http://localhost:8080")

def create_booking(payload: dict) -> dict:
    
    try:
        r = requests.post(f"{BASE}/booking", json=payload, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}
