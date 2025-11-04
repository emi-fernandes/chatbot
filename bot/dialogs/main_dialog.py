from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnStatus
from botbuilder.core import MessageFactory
from .flight_dialog import FlightDialog
from .hotel_dialog import HotelDialog
from .smalltalk_dialog import SmalltalkDialog
from ..core.nlu import infer_intent

class MainDialog(ComponentDialog):
    def __init__(self, user_state):
        super().__init__(MainDialog.__name__)

        # Sub-diálogos
        self.add_dialog(FlightDialog())
        self.add_dialog(HotelDialog())
        self.add_dialog(SmalltalkDialog())

        # Waterfall raiz com 2 passos: roteia -> aguarda finalizar
        self.add_dialog(WaterfallDialog("WF", [self.route_intent, self.final_step]))
        self.initial_dialog_id = "WF"

    async def route_intent(self, step: WaterfallStepContext):
        text = (step.context.activity.text or "").strip()
        intent = infer_intent(text)

        if intent == "flight":
            return await step.begin_dialog("FLIGHT_DIALOG")
        if intent == "hotel":
            return await step.begin_dialog("HOTEL_DIALOG")
        return await step.begin_dialog("SMALLTALK_DIALOG")

    async def final_step(self, step: WaterfallStepContext):
        # Se um sub-diálogo terminou, volta para o início para a próxima mensagem
        await step.context.send_activity(MessageFactory.text("Mais alguma coisa? (voo/hotel)"))
        return await step.end_dialog()
