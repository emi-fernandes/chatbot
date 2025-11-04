from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from ..core.http_client import create_booking

class FlightDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "FLIGHT_DIALOG"):
        super().__init__(dialog_id)
        self.add_dialog(TextPrompt("ORIGIN_PROMPT"))
        self.add_dialog(TextPrompt("DEST_PROMPT"))
        self.add_dialog(TextPrompt("DATE_PROMPT"))
        self.add_dialog(
            WaterfallDialog("WF", [self.ask_origin, self.ask_dest, self.ask_date, self.save_and_end])
        )
        self.initial_dialog_id = "WF"

    async def ask_origin(self, step: WaterfallStepContext):
        return await step.prompt("ORIGIN_PROMPT", PromptOptions(prompt=MessageFactory.text("Qual a cidade de ORIGEM?")))

    async def ask_dest(self, step: WaterfallStepContext):
        step.values["origin"] = (step.result or "").strip()
        return await step.prompt("DEST_PROMPT", PromptOptions(prompt=MessageFactory.text("Destino?")))

    async def ask_date(self, step: WaterfallStepContext):
        step.values["dest"] = (step.result or "").strip()
        return await step.prompt("DATE_PROMPT", PromptOptions(prompt=MessageFactory.text("Data do voo (AAAA-MM-DD)?")))

    async def save_and_end(self, step: WaterfallStepContext):
        date = (step.result or "").strip()
        origin, dest = step.values["origin"], step.values["dest"]

        payload = {
            "type": "flight",
            "userId": step.context.activity.from_property.id if step.context and step.context.activity else "user",
            "detailsJson": f'{{"origin":"{origin}","dest":"{dest}","date":"{date}"}}'
        }

        resp = create_booking(payload)
        if "id" in resp:
            await step.context.send_activity(f"Reserva criada (id {resp['id']}). Buscando opções de {origin} → {dest} em {date}.")
        else:
            await step.context.send_activity(f"Não consegui salvar agora: {resp.get('error','erro desconhecido')}")

        return await step.end_dialog()
