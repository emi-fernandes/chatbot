# app.py
import sys, traceback
from datetime import datetime
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings, TurnContext, BotFrameworkAdapter,
    MemoryStorage, ConversationState, UserState
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes

from bot.main_bot import MainBot
from config import DefaultConfig
from dialogs.main_dialog import MainDialog

CONFIG = DefaultConfig()
print(f"[BOT] JAVA_API_BASE={CONFIG.JAVA_API_BASE} SAVE_TO_DB={CONFIG.SAVE_TO_DB}")

SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID or None, CONFIG.APP_PASSWORD or None)
ADAPTER = BotFrameworkAdapter(SETTINGS)

async def on_error(context: TurnContext, error: Exception):
    print(f"\n[on_turn_error] {error}", file=sys.stderr)
    traceback.print_exc()
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity("To continue to run this bot, please fix the bot source code.")
    if context.activity.channel_id == "emulator":
        await context.send_activity(Activity(
            label="TurnError", name="on_turn_error Trace",
            timestamp=datetime.utcnow(), type=ActivityTypes.trace,
            value=f"{error}", value_type="https://www.botframework.com/schemas/error",
        ))

ADAPTER.on_turn_error = on_error

MEMORY = MemoryStorage()
CONVERSATION_STATE = ConversationState(MEMORY)
USER_STATE = UserState(MEMORY)

DIALOG = MainDialog(USER_STATE)
BOT = MainBot(dialog=DIALOG, conversation_state=CONVERSATION_STATE, user_state=USER_STATE)

async def messages(req: Request) -> Response:
    if "application/json" not in req.headers.get("Content-Type", ""):
        return Response(status=415)
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")
    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=201)

APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(APP, host="localhost", port=CONFIG.PORT)
