from typing import Dict, Any

_SESS: Dict[str, Dict[str, Any]] = {}

def get_session(user_id: str) -> Dict[str, Any]:
    return _SESS.setdefault(user_id, {"current": None, "data": {}})

def set_session(user_id: str, session: Dict[str, Any]) -> None:
    _SESS[user_id] = session
