import os
from dotenv import load_dotenv

load_dotenv()

class DefaultConfig:
    # Porta padrão do Bot Framework Emulator
    PORT = int(os.environ.get("PORT", "3978"))

    # Para rodar local no Emulator, deixe em branco
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    # Base da API Java (Spring Boot)
    JAVA_API_BASE = os.environ.get("JAVA_API_BASE", "http://localhost:8080")

    # Se "true", salva no BD depois da busca (POST /voos ou /hoteis)
    SAVE_TO_DB = os.environ.get("SAVE_TO_DB", "false").lower() == "true"
