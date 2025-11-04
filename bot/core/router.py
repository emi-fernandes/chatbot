from typing import Tuple
from . import nlu, storage
from ..dialogs.root import RootDialog
from ..dialogs.flight import FlightDialog
from ..dialogs.hotel import HotelDialog
from ..dialogs.smalltalk import SmalltalkDialog

DIALOGS = {
    "root": RootDialog(),
    "flight": FlightDialog(),
    "hotel": HotelDialog(),
    "smalltalk": SmalltalkDialog(),
}

def route_message(user_id: str, text: str) -> Tuple[str, bool]:
    sess = storage.get_session(user_id)

    # Se não há diálogo ativo, decidir por intenção
    if not sess.get("current"):
        intent = nlu.infer_intent(text)
        sess["current"] = intent
        sess["data"] = {}
        storage.set_session(user_id, sess)
        return DIALOGS[intent].enter(sess["data"]), False

    # Já há um diálogo ativo
    dialog_name = sess["current"]
    reply, done, new_data = DIALOGS[dialog_name].handle(text, sess["data"])
    sess["data"] = new_data
    if done:
        sess["current"] = None
    storage.set_session(user_id, sess)
    return reply, done
