# bot/dialogs/flight_dialog.py
import re
from botbuilder.core import MessageFactory
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions, PromptValidatorContext
from bot.core.http_client import create_reserva_voo

IATA_RE = re.compile(r"^[A-Za-z]{3}$")

class FlightDialog(ComponentDialog):
    def __init__(self):
        super().__init__(FlightDialog.__name__)

        # prompts com validador IATA
        self.add_dialog(TextPrompt("ORIGIN_PROMPT", FlightDialog._iata_validator))
        self.add_dialog(TextPrompt("DEST_PROMPT", FlightDialog._iata_validator))
        self.add_dialog(TextPrompt("DATE_PROMPT"))  # já está em AAAA-MM-DD

        self.add_dialog(WaterfallDialog(
            "WF",
            [self.ask_origin, self.ask_dest, self.ask_date, self.save_and_end]
        ))
        self.initial_dialog_id = "WF"

    @staticmethod
    async def _iata_validator(ctx: PromptValidatorContext) -> bool:
        text = (ctx.recognized.value or "").strip().upper()
        if IATA_RE.fullmatch(text):
            ctx.recognized.value = text  # normaliza para MAIÚSCULO
            return True
        await ctx.context.send_activity(
            "Por favor, informe o **código IATA** de 3 letras. Exemplos: "
            "`GIG` (Rio Galeão), `SDU` (Santos Dumont), `GRU` (Guarulhos), `CGH` (Congonhas)."
        )
        return False

    async def ask_origin(self, step: WaterfallStepContext) -> DialogTurnResult:
        return await step.prompt(
            "ORIGIN_PROMPT",
            PromptOptions(prompt=MessageFactory.text("Qual o **código IATA** de origem (ex.: GIG/GRU/CGH)?"))
        )

    async def ask_dest(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["origin"] = (step.result or "").strip().upper()
        return await step.prompt(
            "DEST_PROMPT",
            PromptOptions(prompt=MessageFactory.text("Qual o **código IATA** de destino (ex.: GIG/GRU/CGH)?"))
        )

    async def ask_date(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["dest"] = (step.result or "").strip().upper()
        return await step.prompt(
            "DATE_PROMPT",
            PromptOptions(prompt=MessageFactory.text("Data do voo (**AAAA-MM-DD**)?"))
        )

    async def save_and_end(self, step: WaterfallStepContext) -> DialogTurnResult:
        date   = (step.result or "").strip()
        origin = step.values.get("origin", "")
        dest   = step.values.get("dest", "")

        resp = create_reserva_voo(origin, dest, date, airline="BOT", price_brl=0.00)

        if isinstance(resp, dict) and "id" in resp:
            await step.context.send_activity(
                f"✅ Reserva de voo **{resp['id']}** criada.\n"
                f"Rota: **{origin} → {dest}** em **{date}**."
            )
        else:
            await step.context.send_activity(
                "Não consegui salvar agora: "
                f"{resp.get('error','erro desconhecido')}. "
                f"{'Detalhes: ' + resp.get('body','') if isinstance(resp, dict) else ''}"
            )
        return await step.end_dialog()
