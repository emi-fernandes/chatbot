from botbuilder.core import MessageFactory
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions


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
        step.values["checkout"] = (step.result or "").strip()
        city = step.values["city"]; ci = step.values["checkin"]; co = step.values["checkout"]
        await step.context.send_activity(f"Procurando hotéis em **{city}** de **{ci}** a **{co}**…")
        return await step.end_dialog()
