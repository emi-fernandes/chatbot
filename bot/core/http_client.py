import os, json, requests

JAVA_API_BASE = os.getenv("JAVA_API_BASE", "http://localhost:8080")

def create_booking(payload: dict) -> dict:
    """
    Chama o backend Spring (POST /booking) para gravar no Postgres.
    payload esperado: {"type":"flight|hotel","userId":"...","detailsJson":"{...}"}
    """
    url = f"{JAVA_API_BASE}/booking"
    try:
        r = requests.post(url, json=payload, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}
