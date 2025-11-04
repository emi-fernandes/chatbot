# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env", override=True)

def _get_bool(name: str, default: bool = False) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "t", "yes", "y", "on")

class DefaultConfig:
    PORT = int(os.environ.get("PORT", "3978"))

    
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    
    JAVA_API_BASE = os.environ.get("JAVA_API_BASE", "http://localhost:8080")

    
    SAVE_TO_DB = _get_bool("SAVE_TO_DB", False)
