from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext
from botbuilder.core import MessageFactory

class SmalltalkDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "SMALLTALK_DIALOG"):
        super().__init__(dialog_id)
        self.add_dialog(WaterfallDialog("WF", [self.reply]))
        self.initial_dialog_id = "WF"

    async def reply(self, step: WaterfallStepContext):
        await step.context.send_activity(MessageFactory.text("Posso ajudar com voo ✈️ ou hotel 🏨."))
        return await step.end_dialog()
