import os, requests

JAVA_API_BASE = os.getenv("JAVA_API_BASE", "http://localhost:8080")

def create_booking(payload: dict) -> dict:
    url = f"{JAVA_API_BASE}/booking"
    try:
        r = requests.post(url, json=payload, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def get_booking(booking_id):
    url = f"{JAVA_API_BASE}/booking/{booking_id}"
    try:
        r = requests.get(url, timeout=5)
        print("=== RESPOSTA GET /booking ===")
        print("Status:", r.status_code)
        print("Body:", r.text)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        data = r.json()
        # desencaixa {"booking": {...}} se vier assim
        if isinstance(data, dict) and len(data) == 1 and isinstance(next(iter(data.values())), dict):
            data = next(iter(data.values()))
        return data
    except Exception as e:
        return {"error": str(e)}
