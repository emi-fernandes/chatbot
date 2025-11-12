from botbuilder.core import MessageFactory
from botbuilder.dialogs import (
    ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult,
    TextPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
)
from botbuilder.dialogs.choices import Choice
import aiohttp

from bot.config import DefaultConfig  
CONFIG = DefaultConfig()

def _is_int(text: str) -> bool:
    try:
        int(text); return True
    except Exception:
        return False

class ConsultaDialog(ComponentDialog):
    def __init__(self):
        super().__init__(ConsultaDialog.__name__)

        self.add_dialog(TextPrompt("idPrompt"))
        self.add_dialog(ChoicePrompt("tipoPrompt"))
        self.add_dialog(ChoicePrompt("acaoPrompt"))
        self.add_dialog(ConfirmPrompt("confirmPrompt"))

        self.add_dialog(WaterfallDialog("wf", [
            self.perguntar_tipo,
            self.perguntar_id,
            self.perguntar_acao,
            self.confirmar_se_necessario,
            self.executar,
        ]))
        self.initial_dialog_id = "wf"

    async def perguntar_tipo(self, step: WaterfallStepContext) -> DialogTurnResult:
        return await step.prompt(
            "tipoPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Você quer consultar reserva de **voo** ou **hotel**?"),
                choices=[Choice("voo"), Choice("hotel")],
            ),
        )

    async def perguntar_id(self, step: WaterfallStepContext) -> DialogTurnResult:
        step.values["tipo"] = step.result.value  # "voo" | "hotel"
        return await step.prompt(
            "idPrompt",
            PromptOptions(
                prompt=MessageFactory.text("Informe o **ID** da reserva (número)."),
                retry_prompt=MessageFactory.text("ID inválido. Digite apenas números, por favor."),
            ),
        )

    async def perguntar_acao(self, step: WaterfallStepContext) -> DialogTurnResult:
        rid = (step.result or "").strip()
        if not _is_int(rid):
            return await step.replace_dialog(self.id)
        step.values["reserva_id"] = int(rid)

        return await step.prompt(
            "acaoPrompt",
            PromptOptions(
                prompt=MessageFactory.text("O que deseja fazer?"),
                choices=[Choice("detalhes"), Choice("cancelar"), Choice("deletar")],
            ),
        )

    async def confirmar_se_necessario(self, step: WaterfallStepContext) -> DialogTurnResult:
        acao = step.result.value.lower()
        step.values["acao"] = "cancelar" if acao in {"cancelar", "deletar", "excluir", "apagar"} else "detalhes"

        if step.values["acao"] == "cancelar":
            msg = f"Confirma excluir/cancelar a reserva **{step.values['tipo']}** #{step.values['reserva_id']}?"
            return await step.prompt("confirmPrompt", PromptOptions(prompt=MessageFactory.text(msg)))
        return await step.next(True)  # pula confirmação para detalhes

    async def executar(self, step: WaterfallStepContext) -> DialogTurnResult:
        tipo = step.values["tipo"]               # "voo" | "hotel"
        reserva_id = step.values["reserva_id"]   # int
        acao = step.values["acao"]               # "detalhes" | "cancelar"
        base = CONFIG.JAVA_API_BASE.rstrip("/")  # ex: http://localhost:8080

        path = f"/reservas/{'voos' if tipo=='voo' else 'hoteis'}/{reserva_id}"
        url = f"{base}{path}"

        try:
            async with aiohttp.ClientSession() as s:
                if acao == "detalhes":
                    async with s.get(url) as r:
                        if r.status == 200:
                            data = await r.json()
                            await step.context.send_activity(f"📄 Detalhes: {data}")
                        elif r.status == 404:
                            await step.context.send_activity("Reserva não encontrada.")
                        else:
                            await step.context.send_activity(f"Não foi possível obter detalhes. ({r.status})")
                else:
                    # acao == "cancelar"
                    if step.result is not True:  # usuário não confirmou
                        await step.context.send_activity("Cancelamento abortado.")
                        return await step.end_dialog()

                    async with s.delete(url) as r:
                        if r.status in (200, 204):
                            await step.context.send_activity("✅ Reserva cancelada/excluída com sucesso.")
                        elif r.status == 404:
                            await step.context.send_activity("Reserva não encontrada.")
                        else:
                            await step.context.send_activity(f"Não foi possível cancelar. ({r.status})")

        except Exception as e:
            await step.context.send_activity(f"Falha ao contatar a API: {e}")

        return await step.end_dialog()
