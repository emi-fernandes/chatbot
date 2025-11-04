from typing import Tuple, Dict, Any

class Dialog:
    
    name: str = "base"

    def enter(self, session: Dict[str, Any]) -> str:
        return "Como posso ajudar?"

    def handle(self, msg: str, session: Dict[str, Any]) -> Tuple[str, bool, Dict[str, Any]]:
        return "Certo.", True, session
