from typing import Tuple, Dict, Any
from .base import Dialog

class FlightDialog(Dialog):
    name = "flight"

    def enter(self, session):
        session["stage"] = "ask_origin"
        return "Vamos emitir uma passagem. Qual é a cidade de ORIGEM?"

    def handle(self, msg, session) -> Tuple[str, bool, Dict[str, Any]]:
        stage = session.get("stage", "ask_origin")

        if stage == "ask_origin":
            session["origin"] = msg.strip()
            session["stage"]  = "ask_dest"
            return "Destino?", False, session

        if stage == "ask_dest":
            session["dest"] = msg.strip()
            session["stage"] = "ask_date"
            return "Data do voo (AAAA-MM-DD)?", False, session

        if stage == "ask_date":
            session["date"] = msg.strip()
            # Aqui você poderia chamar o backend para registrar intenção de reserva
            session["stage"] = "done"
            reply = f"Perfeito! Procurando voos {session['origin']} → {session['dest']} em {session['date']}."
            return reply, True, session

        return "Certo.", True, session
