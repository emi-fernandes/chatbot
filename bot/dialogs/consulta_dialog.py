from botbuilder.dialogs import (
    ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from bot.core.http_client import get_reserva_voo, get_reserva_hotel


class ConsultaDialog(ComponentDialog):
    def __init__(self):
        super().__init__(ConsultaDialog.__name__)
        self.add_dialog(TextPrompt("TIPO_PROMPT"))
        self.add_dialog(TextPrompt("ID_PROMPT"))
        self.add_dialog(WaterfallDialog("WF", [self.ask_tipo, self.ask_id, self.show]))
        self.initial_dialog_id = "WF"

    async def ask_tipo(self, step: WaterfallStepContext) -> DialogTurnResult:
        return await step.prompt(
            "TIPO_PROMPT",
            PromptOptions(prompt=MessageFactory.text("A reserva é de **voo** ou **hotel**?"))
        )

    async def ask_id(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["tipo"] = (step.result or "").strip().lower()
        return await step.prompt(
            "ID_PROMPT",
            PromptOptions(prompt=MessageFactory.text("Qual o **ID** da sua reserva?"))
        )

    async def show(self, step: WaterfallStepContext) -> DialogTurnResult:
        tipo = step.values["tipo"]
        rid  = (step.result or "").strip()

        if tipo.startswith("vo"):
            resp = get_reserva_voo(rid)
            if isinstance(resp, dict) and "error" in resp:
                await step.context.send_activity(f"❌ Erro ao buscar voo: {resp['error']}")
                return await step.end_dialog()
            if resp is None:
                await step.context.send_activity("❌ Voo não encontrado.")
                return await step.end_dialog()

            msg = [
                "🧾 **Reserva de Voo**",
                f"ID: {resp.get('id', '-')}",
                f"Origem: {resp.get('origin', '-')}",
                f"Destino: {resp.get('destination', '-')}",
                f"Data: {resp.get('date', '-')}",
                f"Companhia: {resp.get('airline', '-')}",
                f"Preço (BRL): {resp.get('priceBRL', '-')}",
                f"Passageiro: {resp.get('passengerName', '-')}",
            ]
            await step.context.send_activity("\n".join(msg))
            return await step.end_dialog()

        if tipo.startswith("ho"):
            resp = get_reserva_hotel(rid)
            if isinstance(resp, dict) and "error" in resp:
                await step.context.send_activity(f"❌ Erro ao buscar hotel: {resp['error']}")
                return await step.end_dialog()
            if resp is None:
                await step.context.send_activity("❌ Hotel não encontrado.")
                return await step.end_dialog()

            msg = [
                "🧾 **Reserva de Hotel**",
                f"ID: {resp.get('id', '-')}",
                f"Cidade: {resp.get('city', '-')}",
                f"Check-in: {resp.get('checkin', '-')}",
                f"Check-out: {resp.get('checkout', '-')}",
                f"Hotel: {resp.get('hotelName', '-')}",
                f"Preço (BRL): {resp.get('priceBRL', '-')}",
                f"Hóspede: {resp.get('guestName', '-')}",
            ]
            await step.context.send_activity("\n".join(msg))
            return await step.end_dialog()

        await step.context.send_activity("Tipo inválido. Digite *voo* ou *hotel*.")
        return await step.end_dialog()
