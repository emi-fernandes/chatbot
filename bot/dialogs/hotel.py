from typing import Tuple, Dict, Any
from .base import Dialog

class HotelDialog(Dialog):
    name = "hotel"

    def enter(self, session):
        session["stage"] = "ask_city"
        return "Vamos reservar um hotel. Em qual cidade?"

    def handle(self, msg, session) -> Tuple[str, bool, Dict[str, Any]]:
        stage = session.get("stage", "ask_city")

        if stage == "ask_city":
            session["city"] = msg.strip()
            session["stage"] = "ask_checkin"
            return "Data de check-in (AAAA-MM-DD)?", False, session

        if stage == "ask_checkin":
            session["checkin"] = msg.strip()
            session["stage"]   = "ask_checkout"
            return "Data de check-out (AAAA-MM-DD)?", False, session

        if stage == "ask_checkout":
            session["checkout"] = msg.strip()
            session["stage"] = "done"
            reply = f"Fechado! Buscando hotéis em {session['city']} de {session['checkin']} a {session['checkout']}."
            return reply, True, session

        return "Certo.", True, session
