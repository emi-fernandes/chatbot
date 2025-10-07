import os
from dotenv import load_dotenv

load_dotenv()

class DefaultConfig:

    PORT = int(os.environ.get("PORT", "3978"))

    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    JAVA_API_BASE = "http://localhost:8080"

    SAVE_TO_DB = os.environ.get("SAVE_TO_DB", "false").lower() == "true"
