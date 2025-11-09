from botbuilder.dialogs import (
    ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from bot.core.http_client import get_booking
import json


class ConsultaDialog(ComponentDialog):
    def __init__(self):
        super().__init__(ConsultaDialog.__name__)
        self.add_dialog(TextPrompt("ID_PROMPT"))
        self.add_dialog(WaterfallDialog("WF", [self.ask_id, self.show_booking]))
        self.initial_dialog_id = "WF"

    async def ask_id(self, step: WaterfallStepContext) -> DialogTurnResult:
        return await step.prompt(
            "ID_PROMPT",
            PromptOptions(prompt=MessageFactory.text("Qual o **ID** da sua reserva?"))
        )

    async def show_booking(self, step: WaterfallStepContext) -> DialogTurnResult:
        booking_id = (step.result or "").strip()
        resp = get_booking(booking_id)

        # falha de rede/servidor
        if isinstance(resp, dict) and "error" in resp:
            await step.context.send_activity(f"❌ Erro ao buscar: {resp['error']}")
            return await step.end_dialog()

        # não encontrado
        if resp is None:
            await step.context.send_activity("❌ Reserva não encontrada.")
            return await step.end_dialog()

        try:
            # detailsJson pode vir como string JSON ou objeto
            details_raw = resp.get("detailsJson") or resp.get("details") or {}
            if isinstance(details_raw, str):
                try:
                    details = json.loads(details_raw)
                except Exception:
                    details = {"raw": details_raw}
            else:
                details = details_raw if isinstance(details_raw, dict) else {"raw": details_raw}

            msg = []
            msg.append("🧾 **Reserva**")
            msg.append(f"ID: {resp.get('id', '(sem id)')}")
            msg.append(f"Tipo: {resp.get('type', '(sem tipo)')}")

            # formatação flexível
            if {"origin", "dest", "date"}.issubset(details.keys()):
                msg += [
                    f"Origem: {details.get('origin', '-')}",
                    f"Destino: {details.get('dest', '-')}",
                    f"Data: {details.get('date', '-')}",
                ]
            elif {"city", "checkin", "checkout"}.issubset(details.keys()):
                msg += [
                    f"Cidade: {details.get('city', '-')}",
                    f"Check-in: {details.get('checkin', '-')}",
                    f"Check-out: {details.get('checkout', '-')}",
                ]
            else:
                # fallback: lista qualquer par chave/valor
                for k, v in details.items():
                    msg.append(f"{k}: {v}")

            await step.context.send_activity("\n".join(msg))

        except Exception as e:
            # mostra conteúdo bruto para depuração se algo fugir do esperado
            await step.context.send_activity(
                f"⚠️ Erro ao processar resposta: {e}\n\nConteúdo retornado:\n```\n{resp}\n```"
            )

        return await step.end_dialog()
