from botbuilder.core import MessageFactory
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from bot.core.http_client import create_reserva_hotel


class HotelDialog(ComponentDialog):
    def __init__(self):
        super().__init__(HotelDialog.__name__)
        self.add_dialog(TextPrompt("CITY_PROMPT"))
        self.add_dialog(TextPrompt("CHECKIN_PROMPT"))
        self.add_dialog(TextPrompt("CHECKOUT_PROMPT"))

        self.add_dialog(WaterfallDialog(
            "WF",
            [self.ask_city, self.ask_checkin, self.ask_checkout, self.finish]
        ))
        self.initial_dialog_id = "WF"

    async def ask_city(self, step: WaterfallStepContext) -> DialogTurnResult:
        return await step.prompt("CITY_PROMPT",
                                 PromptOptions(prompt=MessageFactory.text("Cidade do hotel?")))

    async def ask_checkin(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["city"] = (step.result or "").strip()
        return await step.prompt("CHECKIN_PROMPT",
                                 PromptOptions(prompt=MessageFactory.text("Check-in (AAAA-MM-DD)?")))

    async def ask_checkout(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["checkin"] = (step.result or "").strip()
        return await step.prompt("CHECKOUT_PROMPT",
                                 PromptOptions(prompt=MessageFactory.text("Check-out (AAAA-MM-DD)?")))

    async def finish(self, step: WaterfallStepContext) -> DialogTurnResult:
        city = step.values["city"]
        ci   = step.values["checkin"]
        co   = (step.result or "").strip()

        try:
            resp = create_reserva_hotel(city, ci, co, hotel_name="BOT", price_brl=0.0)
        except Exception as e:
            resp = {"error": str(e)}

        if isinstance(resp, dict) and "id" in resp:
            await step.context.send_activity(
                f"✅ Reserva de hotel **{resp['id']}** criada em **{city}** "
                f"de **{ci}** a **{co}**."
            )
        else:
            err = (resp.get("error") if isinstance(resp, dict) else "erro desconhecido")
            await step.context.send_activity(f"Não consegui salvar agora: {err}")

        return await step.end_dialog()
