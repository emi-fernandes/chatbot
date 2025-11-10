from botbuilder.core import ActivityHandler, TurnContext, ConversationState, UserState, MessageFactory
from botbuilder.dialogs import Dialog
from botbuilder.schema import ActionTypes, CardAction

def make_menu(text: str = "Como posso ajudar?"):
    return MessageFactory.suggested_actions(
        actions=[
            CardAction(title="✈️ Buscar voos",  type=ActionTypes.im_back, value="voo"),
            CardAction(title="🏨 Buscar hotéis", type=ActionTypes.im_back, value="hotel"),
            CardAction(title="📋 Consultas", type=ActionTypes.im_back, value="consultas"),
            CardAction(title="❓ Ajuda", type=ActionTypes.im_back, value="ajuda"),
        ],
        text=text,
    )

class MainBot(ActivityHandler):
    def __init__(self, dialog: Dialog, conversation_state: ConversationState, user_state: UserState):
        self.dialog = dialog
        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog_state = self.conversation_state.create_property("DialogState")

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for m in members_added:
            if m.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Olá! Posso buscar **voos** e **hotéis**.\n"
                    "Exemplos:\n"
                    "• `voo GIG GRU 2025-11-02`\n"
                    "• `hotel Lisboa 2025-11-10 2025-11-12`"
                )
                await turn_context.send_activity(make_menu())

    async def on_message_activity(self, turn_context: TurnContext):
        # lê text e value
        text  = (turn_context.activity.text or "").strip().lower()
        val   = turn_context.activity.value
        if isinstance(val, str):
            val = val.strip().lower()
        msg = val or text

        if msg in ("menu", "/menu"):
            await turn_context.send_activity(make_menu())
            return

        if msg in ("ajuda", "/ajuda", "help", "/help"):
            await turn_context.send_activity(
                "Comandos:\n"
                "• `voo ORIGEM DESTINO DATA(AAAA-MM-DD)`\n"
                "• `hotel CIDADE CHECKIN(AAAA-MM-DD) CHECKOUT(AAAA-MM-DD)`\n"
                "• `menu` • `consultas`"
            )
            await turn_context.send_activity(make_menu("O que deseja fazer agora?"))
            return

        # roda o diálogo principal
        await self.dialog.run(turn_context, self.dialog_state)

        # salva estados
        await self.conversation_state.save_changes(turn_context, False)
        await self.user_state.save_changes(turn_context, False)
