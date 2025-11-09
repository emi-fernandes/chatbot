from botbuilder.core import MessageFactory
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from bot.core.http_client import create_booking


class FlightDialog(ComponentDialog):
    def __init__(self):
        super().__init__(FlightDialog.__name__)

        self.add_dialog(TextPrompt("ORIGIN_PROMPT"))
        self.add_dialog(TextPrompt("DEST_PROMPT"))
        self.add_dialog(TextPrompt("DATE_PROMPT"))

        self.add_dialog(WaterfallDialog(
            "WF",
            [self.ask_origin, self.ask_dest, self.ask_date, self.save_and_end]
        ))
        self.initial_dialog_id = "WF"

    async def ask_origin(self, step: WaterfallStepContext) -> DialogTurnResult:
        return await step.prompt(
            "ORIGIN_PROMPT",
            PromptOptions(prompt=MessageFactory.text("Qual a cidade de **origem**?"))
        )

    async def ask_dest(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["origin"] = (step.result or "").strip()
        return await step.prompt(
            "DEST_PROMPT",
            PromptOptions(prompt=MessageFactory.text("Qual o **destino**?"))
        )

    async def ask_date(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["dest"] = (step.result or "").strip()
        return await step.prompt(
            "DATE_PROMPT",
            PromptOptions(prompt=MessageFactory.text("Data do voo (AAAA-MM-DD)?"))
        )

    async def save_and_end(self, step: WaterfallStepContext) -> DialogTurnResult:
        date   = (step.result or "").strip()
        origin = step.values.get("origin", "")
        dest   = step.values.get("dest", "")

        payload = {
            "type": "flight",
            "userId": step.context.activity.from_property.id if step.context and step.context.activity else "user",
            "detailsJson": f'{{"origin":"{origin}","dest":"{dest}","date":"{date}"}}'
        }

        try:
            resp = create_booking(payload)
        except Exception as e:
            resp = {"error": str(e)}

        if isinstance(resp, dict) and "id" in resp:
            await step.context.send_activity(
                f"✅ Reserva registrada (id **{resp['id']}**).\n"
                f"Buscando opções **{origin} → {dest}** em **{date}**…"
            )
        else:
            err = (resp.get("error") if isinstance(resp, dict) else "erro desconhecido")
            await step.context.send_activity(f"Não consegui salvar agora: {err}")

        return await step.end_dialog()
