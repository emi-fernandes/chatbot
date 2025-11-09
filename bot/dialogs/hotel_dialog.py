from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from bot.core.http_client import create_booking

class HotelDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "HOTEL_DIALOG"):
        super().__init__(dialog_id)
        self.add_dialog(TextPrompt("CITY_PROMPT"))
        self.add_dialog(TextPrompt("CHECKIN_PROMPT"))
        self.add_dialog(TextPrompt("CHECKOUT_PROMPT"))
        self.add_dialog(
            WaterfallDialog("WF", [self.ask_city, self.ask_checkin, self.ask_checkout, self.save_and_end])
        )
        self.initial_dialog_id = "WF"

    async def ask_city(self, step: WaterfallStepContext):
        return await step.prompt("CITY_PROMPT", PromptOptions(prompt=MessageFactory.text("Cidade do hotel?")))

    async def ask_checkin(self, step: WaterfallStepContext):
        step.values["city"] = (step.result or "").strip()
        return await step.prompt("CHECKIN_PROMPT", PromptOptions(prompt=MessageFactory.text("Data de check-in (AAAA-MM-DD)?")))

    async def ask_checkout(self, step: WaterfallStepContext):
        step.values["checkin"] = (step.result or "").strip()
        return await step.prompt("CHECKOUT_PROMPT", PromptOptions(prompt=MessageFactory.text("Data de check-out (AAAA-MM-DD)?")))

    async def save_and_end(self, step: WaterfallStepContext):
        checkout = (step.result or "").strip()
        city, checkin = step.values["city"], step.values["checkin"]

        payload = {
            "type": "hotel",
            "userId": step.context.activity.from_property.id if step.context and step.context.activity else "user",
            "detailsJson": f'{{"city":"{city}","checkin":"{checkin}","checkout":"{checkout}"}}'
        }

        resp = create_booking(payload)
        if "id" in resp:
            await step.context.send_activity(f"Reserva criada (id {resp['id']}). Buscando hotéis em {city} de {checkin} a {checkout}.")
        else:
            await step.context.send_activity(f"Não consegui salvar agora: {resp.get('error','erro desconhecido')}")

        return await step.end_dialog()
