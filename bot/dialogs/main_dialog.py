from botbuilder.core import MessageFactory
from botbuilder.dialogs import (
    ComponentDialog,
    DialogSet,
    DialogTurnStatus,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)

from .flight_dialog import FlightDialog
from .hotel_dialog import HotelDialog
from .consulta_dialog import ConsultaDialog


def _norm(s): 
    return (s or "").strip().lower()


class MainDialog(ComponentDialog):
    def __init__(self):
        super().__init__(MainDialog.__name__)

        # instâncias (guardar para usar .id)
        self.consulta_dialog = ConsultaDialog()
        self.flight_dialog   = FlightDialog()
        self.hotel_dialog    = HotelDialog()

        # registra subdiálogos
        self.add_dialog(self.consulta_dialog)
        self.add_dialog(self.flight_dialog)
        self.add_dialog(self.hotel_dialog)

        # diálogo raiz (roteador)
        self.add_dialog(WaterfallDialog("WF", [self._route_step]))
        self.initial_dialog_id = "WF"

    # >>> necessário pro MainBot chamar self.dialog.run(...)
    async def run(self, turn_context, accessor):
        ds = DialogSet(accessor)
        ds.add(self)
        dc = await ds.create_context(turn_context)
        res = await dc.continue_dialog()
        if res.status == DialogTurnStatus.Empty:
            await dc.begin_dialog(self.id)

    async def _route_step(self, step: WaterfallStepContext) -> DialogTurnResult:
        text  = _norm(getattr(step.context.activity, "text", None))
        value = getattr(step.context.activity, "value", None)
        if isinstance(value, str):
            value = _norm(value)
        msg = value or text

        # --- consultas / cancelamentos ---
        if any(k in msg for k in {
            "consulta","consultas","cancelar","cancelamento","cancelar reserva","ver reserva","minha reserva"
        }):
            return await step.begin_dialog(self.consulta_dialog.id)

        # --- voos ---
        if msg in {"voo","voos","passagem","passagens","flight","flights"}:
            return await step.begin_dialog(self.flight_dialog.id)

        # --- hotéis ---
        if msg in {"hotel","hoteis","hotéis","reserva de hotel","hospedagem"}:
            return await step.begin_dialog(self.hotel_dialog.id)

        # --- menu ---
        if msg in {"menu","/menu"}:
            await step.context.send_activity(MessageFactory.suggested_actions(
                actions=[
                    {"type": "imBack", "title": "✈️ Buscar voos", "value": "voo"},
                    {"type": "imBack", "title": "🏨 Buscar hotéis", "value": "hotel"},
                    {"type": "imBack", "title": "📋 Consultas/Cancelamentos", "value": "consultas"},
                    {"type": "imBack", "title": "❓ Ajuda", "value": "ajuda"},
                ],
                text="Como posso ajudar?",
            ))
            return await step.end_dialog()

        # --- ajuda ---
        if msg in {"ajuda","/ajuda","help","/help"}:
            await step.context.send_activity(
                "Posso buscar **voos** e **hotéis**.\n"
                "Exemplos:\n"
                "• voo GIG GRU 2025-11-02\n"
                "• hotel Lisboa 2025-11-10 2025-11-12\n"
                "Ou digite *menu* para ver os botões."
            )
            return await step.end_dialog()

        # fallback
        await step.context.send_activity(
            "Não entendi. Digite *menu*, *ajuda*, *voo*, *hotel* ou *consultas*."
        )
        return await step.end_dialog()
