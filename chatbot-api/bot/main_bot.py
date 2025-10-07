from botbuilder.core import ActivityHandler, TurnContext, ConversationState, UserState, MessageFactory
from botbuilder.dialogs import Dialog
from botbuilder.schema import SuggestedActions, CardAction, ActionTypes

def make_menu(text: str = "Como posso ajudar?"):
    return MessageFactory.suggested_actions(
        actions=[
            CardAction(title="✈️ Buscar voos",  type=ActionTypes.im_back, value="voo"),
            CardAction(title="🏨 Buscar hotéis", type=ActionTypes.im_back, value="hotel"),
            CardAction(title="📋 Consultas e cancelamentos", type=ActionTypes.im_back, value="consultas"),
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

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        await turn_context.send_activity(
            "Olá! Posso buscar **voos** e **hotéis**.\n"
            "Exemplos:\n"
            "• `voo GIG GRU 02/11/2025`\n"
            "• `hotel Lisboa 10/11/2025 12/11/2025`"
        )
        await turn_context.send_activity(make_menu())

    async def on_message_activity(self, turn_context: TurnContext):
        text = (turn_context.activity.text or "").strip().lower()

        if text in ("menu", "/menu"):
            await turn_context.send_activity(make_menu())
            return
        if text in ("ajuda", "/ajuda", "help", "/help"):
            await turn_context.send_activity(
                "Comandos:\n"
                "• `voo ORIGEM DESTINO DATA(DD/MM/AAAA)`\n"
                "• `hotel CIDADE CHECKIN(DD/MM/AAAA) CHECKOUT(DD/MM/AAAA)`\n"
                "• `menu` para ver botões • `cancelar` • `reiniciar`"
            )
            await turn_context.send_activity(make_menu("O que deseja fazer agora?"))
            return

        await self.dialog.run(turn_context, self.dialog_state)
