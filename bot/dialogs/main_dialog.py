
from __future__ import annotations

import unicodedata
from typing import Optional

from botbuilder.core import MessageFactory, TurnContext
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    TextPrompt,
    DialogTurnStatus,
)


from bot.dialogs.flight_dialog import FlightDialog
from bot.dialogs.hotel_dialog import HotelDialog
from bot.dialogs.smalltalk_dialog import SmalltalkDialog


def _normalize(text: Optional[str]) -> str:
    """minúsculas + remove acentos + tira espaços extras"""
    if not text:
        return ""
    text = text.strip().lower()
    text = "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )
    return " ".join(text.split())


class MainDialog(ComponentDialog):
    """
    Roteador de intents simples:
      - 'voo', 'voos' -> FlightDialog
      - 'hotel', 'hoteis', 'reservar hotel' -> HotelDialog
      - small talk (oi, ola, obrigado...) -> SmalltalkDialog
      - 'menu'/'ajuda' -> mensagens curtas + encerra para o MainBot exibir o menu
      - desconhecido -> dica de uso e encerra
    """

    def __init__(self):
        super().__init__(MainDialog.__name__)

        
        self.add_dialog(TextPrompt("text"))

        self.add_dialog(FlightDialog())     
        self.add_dialog(HotelDialog())      
        self.add_dialog(SmalltalkDialog())  

        self.add_dialog(
            WaterfallDialog(
                "wf",
                [
                    self._route_step,
                    self._final_step,
                ],
            )
        )

        self.initial_dialog_id = "wf"

   
    async def _route_step(self, step: WaterfallStepContext) -> DialogTurnResult:
        text = _normalize(step.context.activity.text)

      
        if text in {"menu", "/menu"}:
            await step.context.send_activity("Abrindo menu…")
            return await step.end_dialog()
        if text in {"ajuda", "/ajuda", "help", "/help"}:
            await step.context.send_activity(
                "Posso buscar **voos** e **hotéis**.\n"
                "Exemplos:\n"
                "• `voo GIG GRU 02/11/2025`\n"
                "• `hotel Lisboa 10/11/2025 12/11/2025`"
            )
            return await step.end_dialog()
        if text in {"cancelar", "/cancelar", "reiniciar", "/reiniciar"}:
            await step.context.send_activity("Conversa reiniciada.")
            return await step.cancel_all_dialogs()

       
        if any(k in text for k in {"voo", "voos", "passagem", "aereo", "aéreo"}):
            return await step.begin_dialog(FlightDialog.__name__)

        if any(k in text for k in {"hotel", "hoteis", "hotels", "hospedagem"}):
            return await step.begin_dialog(HotelDialog.__name__)

        if any(k in text for k in {"oi", "ola", "olá", "bom dia", "boa tarde", "obrigado", "vlw"}):
            return await step.begin_dialog(SmalltalkDialog.__name__)

        
        await step.context.send_activity(
            "Não entendi. Você pode dizer, por exemplo:\n"
            "• `voo GRU GIG 02/12/2025`\n"
            "• `hotel Recife 05/02/2026 09/02/2026`\n"
            "Ou digite `menu` para ver as opções."
        )
        return await step.end_dialog()


    async def _final_step(self, step: WaterfallStepContext) -> DialogTurnResult:
      
        return await step.end_dialog()
