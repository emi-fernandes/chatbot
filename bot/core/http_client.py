# bot/core/http_client.py
import os
import requests

JAVA_API_BASE = os.getenv("JAVA_API_BASE", "http://localhost:8080")

# =======================
# Funções para VOOS
# =======================
def create_reserva_voo(origin: str, destination: str, date: str,
                       airline: str = "BOT", price_brl: float = 0.0,
                       passenger_name: str | None = None):
    """Cria reserva de voo via POST /reservas/voos"""
    url = f"{JAVA_API_BASE}/reservas/voos"
    data = {
        "origin": str(origin or "").upper(),
        "destination": str(destination or "").upper(),
        "date": str(date or ""),
        "airline": str(airline or "BOT"),
        "priceBRL": f"{price_brl:.2f}",
    }
    if passenger_name:
        data["passengerName"] = str(passenger_name)

    r = requests.post(
        url,
        data=data,  # x-www-form-urlencoded
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=8,
    )
    if r.status_code >= 400:
        return {"error": f"{r.status_code} {r.reason}", "body": r.text}
    return r.json()


def get_reserva_voo(reserva_id: str | int):
    """Busca reserva de voo GET /reservas/voos/{id}"""
    url = f"{JAVA_API_BASE}/reservas/voos/{reserva_id}"
    r = requests.get(url, timeout=8)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()


# =======================
# Funções para HOTÉIS
# =======================
def create_reserva_hotel(city: str, checkin: str, checkout: str,
                         hotel_name: str = "BOT", price_brl: float = 0.0,
                         guest_name: str | None = None):
    """Cria reserva de hotel via POST /reservas/hoteis"""
    url = f"{JAVA_API_BASE}/reservas/hoteis"
    data = {
        "city": str(city or ""),
        "checkin": str(checkin or ""),
        "checkout": str(checkout or ""),
        "hotelName": str(hotel_name or "BOT"),
        "priceBRL": f"{price_brl:.2f}",
    }
    if guest_name:
        data["guestName"] = str(guest_name)

    r = requests.post(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=8,
    )
    if r.status_code >= 400:
        return {"error": f"{r.status_code} {r.reason}", "body": r.text}
    return r.json()


def get_reserva_hotel(reserva_id: str | int):
    """Busca reserva de hotel GET /reservas/hoteis/{id}"""
    url = f"{JAVA_API_BASE}/reservas/hoteis/{reserva_id}"
    r = requests.get(url, timeout=8)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()
